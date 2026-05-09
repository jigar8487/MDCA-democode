# Agent Communication Bus

File-based communication system for multi-agent coordination across Claude Code sessions, with Discord thread integration.

## Architecture

```
Discord #wanddy-orchestrator
  |
  User posts: !review PR #452
  |
  v
/discord-check picks it up
  |
  v
Creates Thread on the message: "TASK-001: !review 452"
  |                                    |
  v                                    v
Task file created                 Thread updates posted
  queue/TASK-001.md               [Wanddy] Picked up...
  -> active/TASK-001.md           [Jignesh] Reviewing...
  -> completed/TASK-001.md        [Riya] Tests passed...
                                  [Result] 3 issues found
                                       |
                                  User replies in thread
                                  for discussion
```

## Directory Structure

```
agent-bus/
├── queue/              # Pending tasks from Discord
├── active/             # Currently being worked on
├── completed/          # Done (with results + thread ID)
├── reviews/            # Cross-agent review comments
└── bus.log             # Chronological event log
```

## Task File Format

```markdown
---
id: TASK-20260320-a1b2
requester: jigar
discord_msg_id: 123456789
discord_thread_id: 987654321
created: 2026-03-20 14:30
status: queued | active | completed | failed
assigned_to: jignesh
command: !review 452
priority: medium
---

## Request
!review 452

## Agent Log
[14:30] Wanddy: Picked up, routing to Jignesh
[14:31] Jignesh: Starting PR review
[14:35] Jignesh: Found 3 issues
[14:36] Riya: Running tests - all passed

## Result
3 issues found: missing access rights, no super(), unused import

## Review
Reviewer: hiren
Comments: Architecture looks good, approve with minor fixes
```

## Thread Flow

Every task creates a Discord thread. Updates are posted as the work progresses:

```
#wanddy-orchestrator
|
+-- !review 452                          (original message)
    |
    +-- Thread: "TASK-001: !review 452"
        |-- [Wanddy] Task picked up. Routing to Jignesh...
        |-- [Jignesh] Reviewing PR #452 against .NET + React standards...
        |-- [Jignesh] Found 2 issues in models/res_partner.py
        |-- [Riya] Running automated tests... 176 passed, 0 failed
        |-- [Task Complete] 2 issues found, tests passing
        |-- @jigar can you clarify line 45?     <-- user discussion
        |-- [Jignesh] Line 45: the super() call...  <-- agent responds
```

## Cross-Agent Communication

Agents communicate via:
1. **Task files** — read/write shared state
2. **bus.log** — chronological event stream
3. **reviews/** — structured review comments
4. **Discord threads** — visible to team for discussion

## Commands

| Slash Command | Purpose |
|--------------|---------|
| `/discord-check` | One-time: process all pending Discord commands |
| `/discord-loop 2m` | Continuous: check every 2 minutes |
| `/discord-post #channel message` | Post to any Discord channel |
