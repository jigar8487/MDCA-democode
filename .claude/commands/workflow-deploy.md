# Workflow: Deployment Pipeline

You are orchestrating a deployment for the .NET + React project (.NET 9 + React 18 + TypeScript on Linux/Docker, Nginx reverse proxy, GitHub Actions CI/CD).

**Deployment Request**: "$ARGUMENTS"

---

## Pre-Deployment Phase (Parallel)

### Step 1a: QA Sign-off (`/riya` + `/kavya`)
Launch `/riya` and `/kavya` in parallel:
- `/riya`: Run full automated regression suite (xUnit + Vitest + Playwright via GitHub Actions), report results
- `/kavya`: Confirm manual test coverage, UAT sign-off status
- Output: QA sign-off report

### Step 1b: Code Freeze Validation (`/jignesh`)
Launch `/jignesh` to:
- Verify all GitHub PRs reviewed and approved
- Confirm no pending merge conflicts
- Validate version tagging readiness (semver / release tags)
- Output: Code freeze confirmation

---

## Deployment Phase (Sequential)

### Step 2: Infrastructure Preparation (`/tejas`)
Launch `/tejas` to:
- Verify staging environment matches production config (Docker images, appsettings, Nginx config, environment variables, secrets)
- Prepare backup strategy: `pg_dump` of PostgreSQL + Docker volume snapshots / object-storage backups
- Define deployment steps: build Docker image -> push to GHCR -> pull on target -> `docker compose up -d` (or `systemctl restart`) + `dotnet ef database update` for migrations
- Output: Deployment plan with rollback procedures (image rollback to previous tag, EF migrations rollback)

### Step 3: Staging Deploy (`/tejas`)
Launch `/tejas` to:
- Trigger GitHub Actions deploy workflow targeting staging
- Run smoke tests on staging (health endpoint, key API routes, React app load)
- Validate EF Core migrations apply cleanly without errors
- Output: Staging deployment confirmation

### Step 4: Staging Validation (`/kavya`)
Launch `/kavya` to:
- Execute smoke tests on staging
- Validate critical business flows
- Output: Staging validation report

---

## Go-Live Phase

### Step 5: Go-Live Approval (User)
**STOP AND ASK USER FOR EXPLICIT APPROVAL** before proceeding to production deploy. Summarize:
- Pre-deployment check status
- Staging validation outcome
- Known risks and rollback plan
- Output: User approval (or hold)

### Step 6: Production Deploy (`/tejas`)
**STOP AND ASK USER FOR CONFIRMATION BEFORE THIS STEP**
Launch `/tejas` to:
- Trigger GitHub Actions production deploy workflow (Docker image promotion from staging tag to prod tag)
- Apply EF Core migrations on production
- Restart services: `docker compose restart <service>` or `systemctl restart <service>` and confirm Nginx is healthy
- Monitor for errors via Serilog / journalctl / Docker logs
- Output: Production deployment status

### Step 7: Post-Deploy (`/bhavin` + `/kavya` parallel)
- `/kavya`: Production smoke tests
- `/bhavin`: Client communication, support channel ready
- Output: Post-deploy verification

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

1. Steps 1a, 1b, 1c run in **parallel**
2. Steps 2-7 run **sequentially**
3. **MUST get user confirmation** before Step 6 (production deploy)
4. If any pre-deployment check fails, STOP and report
5. If staging validation fails, STOP and route back to development

## Final Output

```
## Deployment Report

### Target: [staging / production]
### Status: [Success / Failed / Rolled Back]

### Pre-Deployment
| Check | Status | Owner |
|-------|--------|-------|
| QA sign-off | [Pass/Fail] | Riya + Kavya |
| Code freeze | [Pass/Fail] | Jignesh |

### Deployment
| Step | Status | Notes |
|------|--------|-------|
| Backup (pg_dump + volume snapshot) | [Done] | [details] |
| Docker image build + push to GHCR | [Done] | [tag] |
| EF Core migration | [Done] | [details] |
| Service restart (docker compose / systemd) | [Done] | [details] |
| Smoke tests | [Pass] | [details] |

### Post-Deploy
| Verification | Status |
|-------------|--------|
| Smoke tests | [Pass/Fail] |
| Client notified | [Yes/No] |
| Support ready | [Yes/No] |
```
