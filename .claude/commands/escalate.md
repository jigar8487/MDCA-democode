# Escalation Handler

You are handling an escalation for the .NET + React project.

**Escalation**: "$ARGUMENTS"

## Escalation Matrix

Determine the escalation level and route accordingly:

### Level Assessment

| Indicator | Level | Route To |
|-----------|-------|----------|
| Client-reported issue, first response needed | L1 | `/bhavin` |
| Technical issue requiring code investigation | L2 | `/jignesh` |
| Architecture-level issue, systemic problem | L3 | `/hiren` |
| Genuine business ambiguity / scope or commercial decision | L4 | Ask User |

## Execution

1. Assess the escalation level based on the issue description
2. Launch the appropriate sub-agent(s)
3. If the agent identifies it needs escalation to a higher level, chain automatically
4. Always document the escalation trail

## Output

```
## Escalation Report

### Issue: [description]
### Level: [L1-L6]
### Routed To: [team member]
### Status: [Resolved / Escalated / Pending User Input]

### Escalation Trail
| Step | From | To | Reason | Outcome |
|------|------|----|--------|---------|

### Resolution
[what was decided/done]

### Action Items
| # | Action | Owner | Due |
|---|--------|-------|-----|
```
