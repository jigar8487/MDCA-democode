# Discord Command Loop

Continuously monitor #wanddy-orchestrator and process incoming requests. Run `/discord-check` on a recurring interval.

**Interval**: "$ARGUMENTS" (default: 2m)

---

## Instructions

Use the `/loop` skill to run `/discord-check` at the specified interval.

This keeps the Claude Code session actively monitoring Discord for team commands. When a command comes in:
1. It's picked up on the next check cycle
2. Routed to the right sub-agent
3. Executed
4. Result posted back to Discord

To start monitoring: `/discord-loop 2m`
To stop: Press Escape or Ctrl+C

This is the "always-on" mode where the team can continuously send commands via Discord.
