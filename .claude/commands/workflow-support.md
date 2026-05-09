# Workflow: Support Issue Handling

You are orchestrating support issue resolution for the .NET + React project (.NET 9 + React 18 + TypeScript on Linux/Docker).

**Support Issue**: "$ARGUMENTS"

---

## Step 1: First Response & Investigation (`/bhavin`)
Launch a sub-agent with the `/bhavin` skill to:
- Parse the client-reported issue
- Check Serilog logs, journalctl, Docker container logs, Nginx access/error logs, browser console, .NET stack traces, EF Core migration history; reproduce the problem
- Classify severity: P1 (Critical) / P2 (High) / P3 (Medium) / P4 (Low)
- Classify type: Bug / Config / User Error / Enhancement Request
- Output: Investigation report with classification and severity

---

## Route Based on Severity + Type:

### P1 Critical Bug:
**All steps run with URGENCY**

#### Step 2: Immediate Triage (`/jignesh`)
Launch immediately:
- Assess code-level impact
- Identify hotfix approach
- Output: Hotfix plan

#### Step 3: Hotfix (`/aarav`)
Launch immediately after triage:
- Implement minimal fix for the critical issue (backend C# or React TSX)
- Output: Hotfix code

#### Step 4: Emergency Validation (`/kavya`)
- Quick validation of the fix
- Output: Validation result

#### Step 5: Emergency Deploy (`/tejas`)
**ASK USER BEFORE PRODUCTION DEPLOY**
- Build hotfix Docker image, push to GHCR, deploy via GitHub Actions
- Run any required `dotnet ef database update` and `systemctl restart <service>` / `docker compose restart <service>`
- Output: Deploy status

### P2-P3 Bug:
Follow standard `/workflow-bugfix` pipeline

### Config Issue:
#### Step 2: Resolution (`/bhavin`)
- Fix the configuration (appsettings.json, environment variables, Nginx config, Docker compose, systemd unit)
- Document the correct setup
- Output: Resolution + client response

### User Error:
#### Step 2: Documentation (`/bhavin`)
- Prepare clear instructions for the client
- Suggest if user guide update needed
- Output: Client guidance

### Enhancement Request:
#### Step 2: Scope (`/hiren` + `/jignesh` parallel)
- `/hiren`: Capture requirement and architectural impact
- `/jignesh`: Estimate effort, sequencing, and PR plan
- Output: Enhancement proposal

---

## Context Preservation (CRITICAL)

**IMPORTANT**: Long workflows can lose context as the conversation grows. Follow these rules to prevent workflow breakage:

1. **Checkpoint after every step**: After each sub-agent completes, output:
   ```
   CHECKPOINT [Step N]: [step name] -- COMPLETE
   NEXT: Step N+1 -- [description] using /[skill]
   ```
2. **Carry forward only key outputs**: Pass only essential results (decisions, file paths, key findings) to the next step -- not the full sub-agent output
3. **If you lose track**: Check your most recent CHECKPOINT output to determine where you are in the workflow
4. **Keep sub-agent prompts focused**: Give each sub-agent only the context it needs, not the entire workflow history

## Execution Rules

1. Always start with Bhavin (Step 1)
2. P1 issues get immediate parallel execution
3. P2-P4 follow standard workflow timing
4. Always prepare client communication
5. **MUST get user confirmation** for any production hotfix deploy

## Final Output

```
## Support Resolution Report

### Issue: [description]
### Severity: [P1/P2/P3/P4]
### Type: [Bug/Config/User Error/Enhancement]
### Status: [Resolved / In Progress / Escalated]

### Root Cause
[explanation]

### Resolution
[what was done or what is planned]

### Client Communication
[prepared response for the client]

### Prevention
[how to prevent this in the future]
```
