"""
Agent personas as real LLM calls — each invocation is auto-traced as a
Langfuse generation (model, tokens, IO captured) under whatever parent span
the orchestrator opens.

The developer-aarav role actually writes files to disk: the prompt asks for
a JSON envelope with `files: [{path, content}]`, and `agent_act()` parses it
and writes them via the project's repo root. Reviewers (Jignesh, Kavya)
receive the produced files in their context so they review real code, not
just text descriptions.

Usage:
    from agents import agent_act
    r = agent_act(role="developer-aarav", task="Create home.html", context={...})
    # r["text"] = description, r["files_written"] = [paths actually written]

Writes are only under `generated_app/` with allowed extensions; see
`agent_write_guard.ALLOWED_EXTENSIONS`. Path traversal and paths outside
`generated_app/` are rejected.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from langfuse import propagate_attributes

from agent_write_guard import REPO_ROOT, safe_write
from langfuse_setup import langfuse, openrouter_client


ROLE_PROMPTS: dict[str, str] = {
    "developer-aarav": (
        "You are Aarav, a .NET 9 + React 18 + TypeScript Developer on the Wanddy team. "
        "**STACK IS LOCKED to .NET 9 + React 18 + TypeScript.** Anything else (Python, Node, "
        "PHP, plain HTML-only, etc.) is OUT OF SCOPE — return summary='out-of-scope' and "
        "empty files for those.\n\n"
        "For every in-scope request, output ONLY a JSON object (no prose around it):\n\n"
        "{\n"
        '  "slug": "<kebab-case slug derived from the request, e.g. booking-page>",\n'
        '  "files": [{"path": "generated_app/<slug>/<sub>/<file>", "content": "<full file content>"}],\n'
        '  "summary": "<2-3 sentences: what you built and how to run it>"\n'
        "}\n\n"
        "**Mandatory layout** for every new app:\n"
        "  generated_app/<slug>/\n"
        "    backend/                 ← .NET 9 solution\n"
        "      <slug>.Api/\n"
        "        Program.cs           ← minimal API host\n"
        "        Controllers/<Resource>Controller.cs\n"
        "        Models/<Resource>.cs\n"
        "        Services/<Resource>Service.cs\n"
        "        <slug>.Api.csproj    ← targets net9.0\n"
        "      <slug>.sln\n"
        "    frontend/                ← Vite + React 18 + TS, MVC-style SPA\n"
        "      package.json           ← scripts: dev/build/preview\n"
        "      tsconfig.json\n"
        "      vite.config.ts\n"
        "      index.html\n"
        "      src/\n"
        "        main.tsx\n"
        "        App.tsx\n"
        "        models/              ← types + state stores (zustand-style optional)\n"
        "        views/\n"
        "          pages/<page>.tsx\n"
        "          components/<comp>.tsx\n"
        "        controllers/         ← hooks + event handlers (e.g. useXxx.ts)\n"
        "    README.md                ← how to run backend (`dotnet run --project backend/<slug>.Api`) + frontend (`npm install && npm run dev`)\n\n"
        "**Updates to existing apps**: keep all changes inside the same `generated_app/<slug>/` folder.\n\n"
        "Path constraints (the orchestrator enforces these):\n"
        "- Every path MUST start with `generated_app/<slug>/` — no other locations allowed\n"
        "- No `..`, no absolute paths\n"
        "- Allowed extensions: .cs .csproj .sln .ts .tsx .js .jsx .html .css .scss .json .md .yml .yaml .env\n"
        "- Allowed no-ext: Dockerfile, .gitignore, .env.example\n\n"
        "Keep code real and minimal — small but functional. Return JSON only."
    ),
    "tech-lead-jignesh": (
        "You are Jignesh, the Tech Lead and Reviewing Agent. Given the deliverable's file "
        "content, review for code quality, architecture, security, and accessibility. Output "
        "a short bullet list of checks, then either APPROVED or REASSIGN with a specific "
        "rework instruction. ~120 words max."
    ),
    "manual-qa-kavya": (
        "You are Kavya, the Manual QA reviewer. Given the deliverable's file content and "
        "Jignesh's review, perform functional/visual sanity validation. Output pass/fail per "
        "spec point, defect count, sign-off. ~100 words max."
    ),
    "solution-architect-hiren": (
        "You are Hiren, the Solution Architect. Given a request, produce a 1-page spec: "
        "scope, key components, contracts, risks. Hand off to the developer. ~200 words max."
    ),
    "devops-tejas": (
        "You are Tejas, DevOps. Given a deliverable, run/deploy it and report PID, log path, "
        "and health. ~80 words max."
    ),
}


def _extract_json_envelope(text: str) -> dict | None:
    """Pull the first balanced JSON object out of an LLM response, even if
    wrapped in ```json fences or prose."""
    # Strip code fences
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced:
        text = fenced.group(1)
    # Find first balanced {...}
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    for i, ch in enumerate(text[start:], start=start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start : i + 1])
                except json.JSONDecodeError:
                    return None
    return None


def agent_act(
    role: str,
    task: str,
    context: dict[str, Any] | None = None,
    model: str = "openai/gpt-4o-mini",
    max_tokens: int = 512,
) -> dict[str, Any]:
    """
    Run an agent persona as a real LLM call. Returns {text, trace_id}.

    The whole call is wrapped in an `agent`-typed observation; the underlying
    OpenRouter call is auto-traced as a `generation` by Langfuse's OpenAI
    wrapper (model, tokens, IO captured).
    """
    if openrouter_client is None:
        raise RuntimeError("OPENROUTER_API_KEY not set — cannot make LLM call")

    system_prompt = ROLE_PROMPTS.get(role)
    if not system_prompt:
        raise ValueError(f"Unknown role: {role}. Known: {list(ROLE_PROMPTS)}")

    context = context or {}
    user_content = (
        f"Task: {task}\n\n"
        f"Context: {context}\n\n"
        "Respond in your role. Be concise. End with a clear sign-off / handoff line."
    )

    with propagate_attributes(
        tags=[f"role:{role}", "surface:agent-call"],
        metadata=context,
    ), langfuse.start_as_current_observation(
        as_type="agent",
        name=f"agent:{role}",
        input={"task": task, "context": context},
    ) as span:
        # Bigger token budget for developer (it has to emit file content).
        if role == "developer-aarav":
            max_tokens = max(max_tokens, 2000)

        resp = openrouter_client.chat.completions.create(
            name=f"agent-{role}-llm",
            model=model,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
        )
        text = resp.choices[0].message.content or ""

        files_written: list[str] = []
        summary = text

        if role == "developer-aarav":
            envelope = _extract_json_envelope(text)
            if envelope:
                summary = envelope.get("summary", "")
                for f in envelope.get("files", []) or []:
                    target = safe_write(f.get("path", ""), f.get("content", ""))
                    if target:
                        files_written.append(str(target.relative_to(REPO_ROOT)))

        span.update(
            output={"text": text, "files_written": files_written, "summary": summary}
        )

        return {
            "text": text,
            "summary": summary,
            "files_written": files_written,
            "trace_id": langfuse.get_current_trace_id(),
            "role": role,
            "model": model,
        }


def read_files(paths: list[str], max_chars: int = 4000) -> dict[str, str]:
    """Read files (relative to repo root) for reviewer agents."""
    out = {}
    for p in paths:
        f = (REPO_ROOT / p).resolve()
        try:
            f.relative_to(REPO_ROOT)
        except ValueError:
            continue
        if f.is_file():
            content = f.read_text()
            out[p] = content if len(content) <= max_chars else content[:max_chars] + "...[truncated]"
    return out
