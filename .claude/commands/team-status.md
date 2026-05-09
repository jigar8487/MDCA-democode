# Team Status Report

You are generating a comprehensive project status report for the .NET + React project.

**Status Query**: "$ARGUMENTS"

Launch the following sub-agents in **parallel** to gather status from all domains:

## Parallel Status Collection

### Agent 1: Technical Status (`/jignesh`)
- Open PRs and review backlog
- Active development tasks
- Technical debt items
- Code quality metrics

### Agent 2: Architecture Status (`/hiren`)
- Outstanding architectural decisions
- System design risks
- Cross-cutting concerns

### Agent 3: QA Status (`/riya` + `/kavya`)
- Test coverage and pass rates
- Open defects by severity
- Automation coverage percentage
- UAT status

### Agent 4: Support Status (`/bhavin`)
- Open support tickets
- SLA adherence
- Recurring incident patterns

### Agent 5: Infrastructure Status (`/tejas`)
- Environment health
- Deployment pipeline status
- Recent deployments
- Monitoring alerts

---

## Execution Rules

1. Launch ALL 5 agents in parallel
2. Synthesize results into a unified dashboard
3. Highlight blockers and risks prominently
4. Keep the report concise and actionable

## Final Output

```
## The Project Dashboard

### Overall Health: [Green / Yellow / Red]
### Sprint: [name] | Day [X] of [Y]

### Key Metrics
| Metric | Value | Trend |
|--------|-------|-------|
| Sprint progress | [X]% | [up/down/stable] |
| Open PRs | [count] | |
| Open defects | [count] (P1: [n], P2: [n]) | |
| Test pass rate | [X]% | |
| Deployment status | [stable/issues] | |

### Active Blockers
| # | Blocker | Owner | Impact | ETA |
|---|---------|-------|--------|-----|

### Risks
| Risk | Severity | Mitigation | Owner |
|------|----------|------------|-------|

### Action Items
| # | Action | Owner | Due |
|---|--------|-------|-----|

### Recent Activity
[Key updates from the last sprint/week]
```
