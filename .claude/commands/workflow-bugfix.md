# Workflow: Bug Investigation & Fix

You are orchestrating a bug fix pipeline for the .NET + React project (.NET 9 + React 18 + TypeScript on Linux/Docker).

**Bug Report**: "$ARGUMENTS"

Execute this workflow by launching sub-agents with maximum parallelism. Only wait when a step genuinely depends on a previous step's output.

---

## Step 1: Investigation (`/bhavin`)
Launch a sub-agent with the `/bhavin` skill to:
- Parse the bug report and reproduce the issue
- Read relevant code, Serilog logs, journalctl output, Docker container logs, Nginx access/error logs, browser console errors, and .NET stack traces (e.g., `System.NullReferenceException at App.Api.Controllers.OrdersController.PostAsync (line 87)`) or React error boundary output
- Classify the issue: **Bug** / **New Requirement** / **Config Issue** / **User Error**
- Identify root cause and affected projects (Api / Domain / Application / Infrastructure / Web frontend)
- Output: Investigation report with classification

---

## Branch Based on Classification:

### If BUG:

#### Step 2: Regression Test + Triage (Parallel)

##### Step 2a: Regression Test (`/riya`)
Launch `/riya` to:
- Write a failing test that proves the bug exists (xUnit for backend, Vitest/RTL for React, Playwright for E2E)
- Define expected correct behavior
- Output: Failing test case

##### Step 2b: Triage (`/jignesh`)
Launch `/jignesh` **in parallel** with `/riya` to:
- Assess severity and impact
- Define fix approach and affected code paths (controllers, services, EF Core queries, React components)
- Output: Triage report with fix strategy

#### Step 3: Fix (`/aarav`)
Using Riya's test + Jignesh's triage, launch `/aarav` to:
- Fix the root cause (not a workaround)
- Ensure Riya's test now passes
- Follow GitHub PR workflow
- Output: Fix code + passing test

#### Step 4: Validation (`/kavya`)
Launch `/kavya` to:
- Verify the fix resolves the original issue
- Check for regression in related functionality
- Output: Validation report

### If NEW REQUIREMENT:

#### Step 2: Architectural Scoping (`/hiren` + `/jignesh`)

##### Step 2a: Architecture impact (`/hiren`)
Launch `/hiren` to:
- Capture the requirement and target acceptance criteria from a system-design lens
- Flag impact on .NET solution structure, EF Core schema, React module boundaries
- Output: Architecture impact note

##### Step 2b: Effort + sequencing (`/jignesh`)
Launch `/jignesh` **in parallel** with `/hiren` to:
- Estimate development effort and sequencing risk
- Flag PR/branching implications and downstream test load
- Output: Impact assessment

### If CONFIG ISSUE / USER ERROR:

#### Step 2: Resolution (`/bhavin`)
Continue with `/bhavin` to:
- Fix configuration (appsettings.json, environment variables, Nginx config, Docker compose) or document the correct process
- Prepare client communication
- Output: Resolution + client response

---

## Context Preservation (CRITICAL)

**IMPORTANT**: Long workflows can lose context as the conversation grows. Follow these rules to prevent workflow breakage:

1. **Checkpoint after every step**: After each sub-agent completes, output:
   ```
   CHECKPOINT [Step N]: [step name] -- COMPLETE
   KEY OUTPUTS: [1-2 line summary]
   NEXT: Step N+1 -- [description] using /[skill]
   ```
2. **Carry forward only key outputs**: Pass only essential results (decisions, file paths, key findings) to the next step -- not the full sub-agent output
3. **If you lose track**: Check your most recent CHECKPOINT output to determine where you are in the workflow
4. **Keep sub-agent prompts focused**: Give each sub-agent only the context it needs, not the entire workflow history

## Execution Rules

1. Always start with Step 1 (investigation)
2. Branch based on Bhavin's classification
3. For BUG path: Steps 2a+2b run in **parallel**, then Step 3, then Step 4
4. For NEW REQUIREMENT: Steps 2a+2b run in **parallel**
5. For CONFIG/USER ERROR: Step 2 only
6. Always end with a summary for the user

## Final Output

```
## Bug Fix Report

### Issue: [description]
### Classification: [Bug / Requirement / Config / User Error]
### Root Cause: [explanation]
### Resolution: [what was done]

### Files Changed
| File | Change | Reason |
|------|--------|--------|
| [path] | [change] | [why] |

### Tests
| Test | Status |
|------|--------|
| [test name] | [Pass/Fail] |

### Verification: [Passed / Pending]
```
