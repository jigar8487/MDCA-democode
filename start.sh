#!/usr/bin/env bash
# Wanddy system — start everything
set -e
cd "$(dirname "$0")"

# 1. Load env (Discord, OpenRouter, Langfuse keys)
set -a; source .env; set +a

# 2. Make sure deps are installed (idempotent — pip will skip if up-to-date)
pip3 install -q -r requirements.txt

# 3. Start the gateway daemon (Wanddy bot online presence in Discord)
mkdir -p .claude/agent-bus
PID_FILE=.claude/agent-bus/wanddy_presence.pid
LOG_FILE=.claude/agent-bus/wanddy_presence.log
if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "🟢 gateway already running (PID $(cat "$PID_FILE"))"
else
  nohup python3 wanddy_presence.py > "$LOG_FILE" 2>&1 &
  echo $! > "$PID_FILE"
  sleep 2
  if kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "🟢 gateway started (PID $(cat "$PID_FILE"))"
    head -1 "$LOG_FILE"
  else
    echo "❌ gateway failed to start — see $LOG_FILE"
    exit 1
  fi
fi

# 4. Run one orchestrator tick now to catch up on anything that arrived
#    in Discord while we were offline (state file on disk → resumes cleanly)
echo "▶︎ running one orchestrator tick to catch up..."
python3 wanddy_orchestrator.py
echo

cat <<EOF
✅ System started.

To resume the cron loop in Claude Code, run:
   /loop 1m check discord message in wanddy-orchestrator channel and assign each message to him. He will assign this to right person and planner agent will do each request planning first than assign will work.

State files (preserved across restarts):
  .claude/agent-bus/orchestrator_state.json  — tracked Discord requests
  .claude/agent-bus/status_board_message_id.txt — sticky status board
  .claude/agent-bus/memory/                 — learned patterns + users

To stop: ./stop.sh
EOF
