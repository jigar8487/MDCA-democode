#!/usr/bin/env bash
# Wanddy system — stop everything (state on disk is preserved)
cd "$(dirname "$0")"

PID_FILE=.claude/agent-bus/wanddy_presence.pid
if [ -f "$PID_FILE" ]; then
  PID=$(cat "$PID_FILE")
  if kill -0 "$PID" 2>/dev/null; then
    kill "$PID"
    sleep 1
    if kill -0 "$PID" 2>/dev/null; then
      kill -9 "$PID"
    fi
    echo "🛑 gateway stopped (was PID $PID)"
  else
    echo "ℹ️  gateway PID $PID was already dead"
  fi
  rm -f "$PID_FILE"
else
  echo "ℹ️  no gateway PID file — nothing to stop"
fi

echo "ℹ️  cron loop is session-only; it stops when Claude session ends."
echo "✅ Stopped. State preserved on disk; ./start.sh to resume."
