"""
Langfuse initialization for the demo project.

Loads credentials from .env, returns a configured Langfuse client, and
provides two LLM clients — both auto-traced as Langfuse generations:

  * `openrouter_client` — Langfuse OpenAI wrapper pointed at OpenRouter
    (model names like "anthropic/claude-3.5-sonnet", "openai/gpt-4o-mini").
    Use this when only OPENROUTER_API_KEY is available.

  * `anthropic_client`  — direct Anthropic SDK auto-instrumented via
    AnthropicInstrumentor. Use this when ANTHROPIC_API_KEY is available.

Both are auto-traced. Pick whichever your env supplies a key for.

Usage:
    from langfuse_setup import langfuse, openrouter_client, assert_credentials_ok
    assert_credentials_ok()
    resp = openrouter_client.chat.completions.create(
        model="anthropic/claude-3.5-sonnet",
        messages=[{"role": "user", "content": "Hi"}],
    )
    langfuse.flush()  # call before the script exits
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

# 1. Load env BEFORE importing langfuse (per skill guidance — wrong order is a
#    common mistake that silently initializes Langfuse with missing credentials).
load_dotenv()

# 2. Normalize host env var. The Python SDK reads LANGFUSE_HOST; this project's
#    .env uses LANGFUSE_BASE_URL. Mirror it (and strip trailing slash) so traces
#    land in the configured region (e.g. JP cloud) instead of the EU default.
if not os.environ.get("LANGFUSE_HOST") and os.environ.get("LANGFUSE_BASE_URL"):
    os.environ["LANGFUSE_HOST"] = os.environ["LANGFUSE_BASE_URL"].rstrip("/")

# 3. Normalize OpenRouter key env var. The .env uses `OpenRouter_Key`; both
#    the OpenAI SDK and our planner code expect OPENROUTER_API_KEY.
if not os.environ.get("OPENROUTER_API_KEY") and os.environ.get("OpenRouter_Key"):
    os.environ["OPENROUTER_API_KEY"] = os.environ["OpenRouter_Key"]

# 2. Import Langfuse, then instrument Anthropic, then import the Anthropic
#    client. Order matters: instrumentation must be active before the patched
#    client is used.
from langfuse import get_client  # noqa: E402
from langfuse.openai import OpenAI as LangfuseOpenAI  # noqa: E402
from opentelemetry.instrumentation.anthropic import AnthropicInstrumentor  # noqa: E402

AnthropicInstrumentor().instrument()

from anthropic import Anthropic  # noqa: E402


langfuse = get_client()

# Anthropic direct (auto-traced by AnthropicInstrumentor) — only usable when
# ANTHROPIC_API_KEY is set; otherwise importing/using will raise at call time.
anthropic_client = Anthropic() if os.environ.get("ANTHROPIC_API_KEY") else None

# OpenRouter via Langfuse's OpenAI wrapper — auto-traced as a generation with
# model name, tokens, IO. OpenRouter is OpenAI-API-compatible so the wrapper
# works with no code changes vs. plain OpenAI.
openrouter_client = (
    LangfuseOpenAI(
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1",
    )
    if os.environ.get("OPENROUTER_API_KEY")
    else None
)


def assert_credentials_ok() -> None:
    """Raise if Langfuse credentials are missing or wrong. Call once at startup."""
    if not langfuse.auth_check():
        raise RuntimeError(
            "Langfuse auth_check failed. Verify LANGFUSE_PUBLIC_KEY / "
            "LANGFUSE_SECRET_KEY / LANGFUSE_BASE_URL in .env."
        )
