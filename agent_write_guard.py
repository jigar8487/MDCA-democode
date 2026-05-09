"""
Path rules for LLM-driven writes under `generated_app/`. Kept separate from
`agents.py` so tests and tooling can import without Langfuse/OpenTelemetry.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
GENERATED_APP_DIR = REPO_ROOT / "generated_app"
ALLOWED_EXTENSIONS = {
    # .NET backend
    ".cs",
    ".csproj",
    ".sln",
    ".json",
    ".props",
    ".targets",
    # React/TS frontend
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".html",
    ".css",
    ".scss",
    # Common
    ".md",
    ".txt",
    ".yml",
    ".yaml",
    ".env",
    ".gitignore",
}
ALLOWED_NO_EXT_NAMES = {"Dockerfile", ".dockerignore", ".env.example", ".gitignore"}


def safe_write(rel_path: str, content: str) -> Path | None:
    """Write to REPO_ROOT/rel_path if under generated_app/ and allowed.

    Returns resolved Path on success, None on rejection (traversal, wrong
    root, disallowed extension).
    """
    if not rel_path or rel_path.startswith("/") or ".." in Path(rel_path).parts:
        return None
    repo_root = REPO_ROOT.resolve()
    generated_base = GENERATED_APP_DIR.resolve()
    target = (repo_root / rel_path).resolve()
    try:
        target.relative_to(generated_base)
    except ValueError:
        return None
    suffix = target.suffix.lower()
    name = target.name
    if suffix not in ALLOWED_EXTENSIONS and name not in ALLOWED_NO_EXT_NAMES:
        return None
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    return target
