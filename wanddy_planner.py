"""
Wanddy Planner Agent — Anthropic + Langfuse traced.

This is the LLM surface that mirrors the Wanddy "planner" step from the
Discord-orchestrator skill: take a user request from #wanddy-orchestrator,
produce a structured plan (subtasks + agent allocation) the user can approve.

Tracing follows the Langfuse instrumentation skill's baseline + extras:
- Auto-instrumented Anthropic generation (model name, tokens, IO captured)
- Descriptive trace + span names (`wanddy-planner`, not `trace-1`)
- session_id      — Discord thread ID groups conversation turns
- user_id         — Discord user ID for per-user filtering
- tags            — `feature:wanddy-planner`, `source:discord`
- metadata        — Jira project, request hash for correlation
- Explicit input  — only the user message (not all function args / API keys)
- flush()         — before exit so traces are sent

Run:
    ANTHROPIC_API_KEY=sk-ant-... python3 wanddy_planner.py
If ANTHROPIC_API_KEY is missing, falls back to a manual generation span so
the trace structure is still demonstrable end-to-end.
"""

from __future__ import annotations

import hashlib
import os
import sys
from typing import Any

from langfuse import propagate_attributes

from langfuse_setup import (
    anthropic_client,
    assert_credentials_ok,
    langfuse,
    openrouter_client,
)

PLANNER_SYSTEM_PROMPT = """You are the Wanddy Planner Agent. A user posted a request in the team's Discord orchestrator channel. Your job is to decompose the request into a sequential agent plan that the orchestrator can execute.

Constraints:
- Jira project key and board are configured per deployment (see environment / docs). Use a sensible status pipeline: TO-DO → IN PROGRESS → IN REVIEW → DONE.
- Naming pattern for agent-owned issues: {Agent}-{IssueKey}-{Title}.
- Agents available: Hiren (architect), Aarav (dev), Jignesh (TL/reviewer), Kavya (QA reviewer), Tejas (DevOps), Yash (integration), Riya (QA automation), Bhavin (support).
- Subtasks execute strictly sequentially.
- The Reviewing Agent has reassign authority (can send back to IN PROGRESS).

Output format: JSON with keys `subtasks` (list of {title, owner, stage}), `reviewing_agent`, `clarifying_questions` (list, may be empty), and `notes` (one short paragraph)."""


def plan_request(
    user_message: str,
    discord_user_id: str,
    discord_thread_id: str,
    model: str | None = None,
    max_tokens: int = 1024,
) -> dict[str, Any]:
    """
    Produce a Wanddy plan for a Discord request. Auto-traced as a Langfuse
    generation. Uses (in order of preference): OpenRouter (via Langfuse's
    OpenAI wrapper), Anthropic direct (via AnthropicInstrumentor), or a stub.

    Returns: {trace_id, trace_url, plan_text}
    """
    request_hash = hashlib.sha256(user_message.encode()).hexdigest()[:12]

    # Trace-level correlating attrs (v4: propagate_attributes context manager).
    # These auto-propagate to every observation created in the scope.
    with propagate_attributes(
        trace_name="wanddy-planner",
        user_id=discord_user_id,
        session_id=discord_thread_id,
        tags=["feature:wanddy-planner", "source:discord"],
        metadata={
            "jira_project": os.environ.get("JIRA_PROJECT_KEY", "PROJ"),
            "request_source": "discord",
            "request_hash": request_hash,
        },
    ), langfuse.start_as_current_observation(
        as_type="agent",
        name="wanddy-planner",
        input={"user_message": user_message},  # explicit — don't leak function args
    ) as span:
        if openrouter_client is not None:
            # Preferred path: OpenRouter via Langfuse's OpenAI wrapper.
            # Auto-traced as a generation with model name, tokens, IO.
            chosen_model = model or "openai/gpt-4o-mini"
            resp = openrouter_client.chat.completions.create(
                name="wanddy-planner-llm",
                model=chosen_model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
            )
            plan_text = resp.choices[0].message.content or ""
        elif anthropic_client is not None:
            # Fallback: Anthropic direct, auto-traced by AnthropicInstrumentor.
            chosen_model = model or "claude-sonnet-4-5"
            message = anthropic_client.messages.create(
                model=chosen_model,
                max_tokens=max_tokens,
                system=PLANNER_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_message}],
            )
            plan_text = "".join(
                block.text for block in message.content if getattr(block, "type", None) == "text"
            )
        else:
            # Last resort stub for runs without any LLM key.
            chosen_model = model or "stub"
            plan_text = (
                "[STUB — set OPENROUTER_API_KEY or ANTHROPIC_API_KEY for real planning] "
                "Sample plan: 1) Aarav-PROJ-X-Implement, 2) Jignesh-PROJ-Y-Review, "
                "3) Kavya-PROJ-Z-UAT. Reviewing Agent: Jignesh."
            )
            with langfuse.start_as_current_observation(
                as_type="generation",
                name="planner-stub",
                model=chosen_model,
                input=[{"role": "user", "content": user_message}],
                metadata={"reason": "no LLM key set — stub response"},
            ) as gen:
                gen.update(output=plan_text, usage_details={"input": 0, "output": 0})

        span.update(output={"plan": plan_text})

        trace_id = langfuse.get_current_trace_id()
        trace_url = langfuse.get_trace_url(trace_id=trace_id)

    return {"trace_id": trace_id, "trace_url": trace_url, "plan_text": plan_text}


def main() -> int:
    assert_credentials_ok()

    sample = {
        "user_message": "Example: create a task in Jira for a PM agent skill.",
        "discord_user_id": os.environ.get("PLANNER_SAMPLE_DISCORD_USER_ID", "000000000000000000"),
        "discord_thread_id": os.environ.get(
            "PLANNER_SAMPLE_DISCORD_THREAD_ID", "000000000000000001"
        ),
    }

    result = plan_request(**sample)
    print(f"Trace ID:  {result['trace_id']}")
    print(f"Trace URL: {result['trace_url']}")
    if os.environ.get("OPENROUTER_API_KEY"):
        mode = "live (OpenRouter)"
    elif os.environ.get("ANTHROPIC_API_KEY"):
        mode = "live (Anthropic)"
    else:
        mode = "stub (no LLM key set)"
    print(f"Mode:      {mode}")
    print(f"Plan:      {result['plan_text'][:120]}...")

    langfuse.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
