#!/usr/bin/env bash
# Single Wanddy tick: runs the instrumented Python orchestrator so each tick
# emits Langfuse traces. Driven by the Claude Code /loop cron.
set -e
cd "$(dirname "$0")"
set -a
source .env
set +a
export LANGFUSE_HOST="${LANGFUSE_BASE_URL%/}"
python3 wanddy_orchestrator.py
