# Learned Patterns

Patterns learned from Discord interactions. Updated after each task.

## Wanddy Workflow Conventions (Active — v2 spec, authoritative)

**Updated**: 2026-05-08 by user via diagram + requirements doc (supersedes earlier free-form spec).

### Canonical per-iteration flow
Single control point: **Wanddy**. Repeats for every Discord request.

```
Discord (user submits)                              [Jira: TO-DO]
        │
        ▼
Wanddy (receives, assigns to Planner)
        │
        ▼
Planner Agent (decomposes goal, allocates subtasks to relevant agents)
        │
        ▼
Wanddy (plan returned, then instructs agents ONE BY ONE)
        │
        ▼
Agent A → Agent B → ... → Agent N (each executes)  [Jira: IN PROCESS]
        │
        ▼
Reviewing Agent (evaluates; may REASSIGN to another agent → loops back to IN PROCESS)
        │                                            [Jira: IN REVIEW]
        ▼ (approve)
Task marked Done                                     [Jira: DONE]
        │
        ▼
Wanddy (receives final status update)
        │
        ▼ (if more iteration needed)
Loop back to step 1
```

### Typing + heartbeat (user assurance — never go silent)
Discord typing auto-clears after ~10s. Multi-phase workflows have gaps between posts; without active management the user sees nothing for 30+ seconds and assumes the bot is dead.

**Mandatory pattern** for any multi-phase iteration:

1. **At the start of every phase**, fan out a typing fire to ALL relevant channels at once (originating thread + each agent channel that will post that phase):
```bash
for CH in <thread> <agent_channel_1> <agent_channel_2>; do
  curl -s -X POST "https://discord.com/api/v10/channels/$CH/typing" -H "Authorization: Bot $DISCORD_TOKEN" -o /dev/null
done
```

2. **If a phase is expected to exceed 10s** (Plan agent calls, large Jira batches), kick off a background heartbeat:
```bash
( while true; do
    for CH in <thread> <agent_channel>; do
      curl -s -X POST "https://discord.com/api/v10/channels/$CH/typing" -H "Authorization: Bot $DISCORD_TOKEN" -o /dev/null
    done
    sleep 8
  done ) & TYPING_PID=$!
# ... do work ...
kill $TYPING_PID 2>/dev/null
```

3. **If a phase will exceed 30s**, also post a brief progress message in the originating thread (don't rely on typing alone):
```
**[Wanddy]** ⏳ Still working on this — <phase>. Next update in ~30s.
```

4. **Cron-driven iterations**: at the START of each cron tick, if there's an in-flight task (any issue key in IN PROGRESS or IN REVIEW), fire typing on the relevant thread + agent channel before doing scan work. This keeps the indicator alive across cron ticks.

5. **At the end of every phase, post the result message immediately** — never end a phase silently. Even a "phase X done, starting phase Y" message is better than dead air.

### Strict rules
1. **Planner Agent is explicit and mandatory** — Wanddy MUST hand off to the Planner before assigning agents. Planner produces the subtask list + agent allocation. No bypassing this step.
2. **Sequential agent execution** — Wanddy instructs agents one-by-one, NOT in parallel, even when subtasks are independent. (This supersedes the earlier "parallel where independent" pattern.)
3. **Reviewing Agent is a distinct role** — applied at IN REVIEW. Pick by task domain: Jignesh (TL) for code/architecture, Kavya (QA) for functional, Hiren (SA) for design, etc. The reviewer has authority to REASSIGN to another agent, which sends the task back to IN PROCESS under the new owner.
4. **Wanddy is the single control point** — every state transition (TO-DO → IN PROCESS → IN REVIEW → DONE) flows through Wanddy. Wanddy posts board updates after each transition in the originating thread.
5. **Each agent posts in their own channel** on pickup, completion, and reassignment (channel IDs listed below).



### Jira issue naming pattern
Every agent-owned issue must be titled `{Agent}-{IssueKey}-{Title}`.
- Example: `Hiren-PROJ-6-Define PM agent scope, tools, and skill description`
- Why: agents are not real Jira users; the prefix makes ownership scannable on the board.
- Apply to: subtasks (and any issue type assigned to a single agent). Parent stories/epics may stay un-prefixed.

### Status flow (example Jira workflow)
`To Do → In Progress → In Review → Done`
- "In Review" is often used as the **UAT** stage when the project has no native "UAT" status.
- An agent moves a task from `To Do` → `In Progress` when they pick it up.
- An agent moves it to `In Review` when they hand off / complete primary work.
- Reviewer (or Wanddy after sign-off) moves to `Done`.
- Transition IDs are **site-specific**; read them from your Jira Cloud workflow (do not hardcode cloud IDs in shared docs).

### Agent Discord channels (post status here on every transition)
Each agent's own channel under the **AGENTS** category — they MUST post when picking up, completing, or blocking on a task.
Map channels via environment variables (see `.claude/commands/discord-post.md`), e.g. `DISCORD_CHANNEL_SOLUTION_ARCHITECT_HIREN`, `DISCORD_CHANNEL_DEVELOPER_AARAV`, etc.

Wanddy posts the orchestration summary (board state, hand-offs) into the originating thread under #wanddy-orchestrator.

### Loop behavior
On every cron tick:

1. **Run the traced Python orchestrator first**: `python3 wanddy_orchestrator.py`
   - Scans #wanddy-orchestrator + active threads
   - For each new message: creates thread, posts ack, calls traced planner (`wanddy_planner.py` via OpenRouter), creates Jira placeholder, posts plan
   - For each thread reply: classifies (approve/reject/modify), updates state
   - Every step is a Langfuse span — the whole iteration is one trace tree
   - State persisted at `.claude/agent-bus/orchestrator_state.json`

2. After the Python orchestrator runs, if any state entry is `approved-pending-execution`, drive the v2 subtask execution (rename, transitions, agent posts) — this part is still manual orchestration in this Claude session for now (Phase-2 to migrate).

3. For each subtask in `To Do` whose dependencies (description "Blocked by:" line) are `Done` or `In Review`, the next available agent picks it up: transition to `In Progress` + post pickup message in that agent's channel.
4. For each `In Progress` subtask owned by an agent who has produced a deliverable (comment), transition to `In Review` + post completion message.
5. Wanddy posts a board-state summary in the originating thread when any state changes.

## Common Issues & Solutions

(Auto-populated as issues are resolved)

### Template
```
### Pattern: {short description}
- **First Seen**: {date}
- **Frequency**: {how many times this came up}
- **Symptoms**: {what the user reports}
- **Root Cause**: {what actually caused it}
- **Solution**: {how it was fixed}
- **Prevention**: {how to prevent it in future}
- **Related Files**: {files involved}
```

## Common Questions & Answers

(Auto-populated as questions are answered)

### Template
```
### Q: {question}
- **Answer**: {concise answer}
- **Asked By**: {users who asked this}
- **Times Asked**: {count}
- **Related Docs**: {links to relevant documentation}
```

## Rejected/Irrelevant Messages Log

(Track messages that were out of scope to improve filtering)

### Template
```
### {date} | {user} | Relevance: {LOW/ZERO}
- **Message**: {what they said}
- **Why Irrelevant**: {reason}
- **Response Given**: {what Wanddy replied}
```

### [LEGACY — pre-migration] Pattern: Settings form crash on cross-project foreign key
- **First Seen**: 2026-03-20
- **Frequency**: 1
- **Status**: Historical pattern from prior platform; preserved for reference. Not applicable to current .NET 9 + React 18 stack.
- **Symptoms** (legacy): Frontend null-reference crash when clicking Settings
- **Root Cause** (legacy): UI compiler crashed when a foreign-key widget referenced a model from an optional dependency
- **Equivalent risk on current stack**: A React component depending on optional API data should guard against `undefined`; in EF Core, optional cross-context references should be modeled as nullable FKs with proper null handling in DTOs.
