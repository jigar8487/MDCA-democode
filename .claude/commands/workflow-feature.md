# Workflow: New Feature Development (End-to-End)

You are orchestrating a full feature development pipeline for the .NET + React project (.NET 9 + React 18 + TypeScript on Linux/Docker).

**Feature Request**: "$ARGUMENTS"

Execute this workflow by launching sub-agents with maximum parallelism. Only wait when a step genuinely depends on a previous step's output.

---

## Phase 1: Architecture (`/hiren`)

Launch `/hiren` to:
- Capture feature scope, target acceptance criteria, and key data entities
- Design solution architecture (Api / Domain / Application / Infrastructure / Web projects, EF Core entities, repositories, services)
- Define database schema (PostgreSQL via EF Core), integration points, React component structure
- Ensure upgrade-safe, multi-tenant-ready design
- Output: Architecture blueprint with acceptance criteria

---

## Phase 2: Technical Plan (`/jignesh`)

Using Phase 1 output, launch `/jignesh` to:
- Break the architecture into developer-ready technical tasks (controllers, services, EF Core entities, React components, authorization policies)
- Estimate effort, sequence work, and call out PR / branching strategy
- Identify cross-cutting risks and dependencies
- Output: Task breakdown with estimates

---

## Phase 3: Development (Sequential — code depends on architecture)

### Step 3: Test-First + Development (`/riya` then `/jignesh` + `/aarav`)
1. Launch `/riya` to write automated test cases (xUnit for backend, Vitest + React Testing Library for frontend, Playwright for E2E) based on Phase 1 requirements
2. Then launch `/jignesh` to plan technical approach (controllers, services, EF Core entities, React components, authorization policies)
3. Then launch `/aarav` to implement entities, controllers, services, React components, authorization, migrations — code must pass Riya's tests
- Output: Test suite + complete .NET solution + React app code

---

## Phase 4: Quality Assurance + Deployment (Parallel)

### Step 4a: Manual QA (`/kavya`)
Launch `/kavya` to:
- Create manual test cases from functional spec
- Execute exploratory testing scenarios
- Output: Manual test report

### Step 4b: Code Review (`/jignesh`)
Launch `/jignesh` **in parallel** with `/kavya` to:
- Review C# and TypeScript code against standards
- Validate architecture compliance
- Output: Code review report

### Step 4c: Deployment Plan (`/tejas`)
Launch `/tejas` **in parallel** with `/kavya` and `/jignesh` to:
- Prepare GitHub Actions pipeline + Docker image deployment configuration
- Define staging validation steps (Linux server, Nginx reverse proxy, EF Core migrations)
- Output: Deployment plan

---

## Context Preservation (CRITICAL)

**IMPORTANT**: Long workflows can lose context as the conversation grows. Follow these rules to prevent workflow breakage:

1. **Checkpoint after every phase**: After each phase completes, output:
   ```
   CHECKPOINT [Phase N]: [phase name] -- COMPLETE
   KEY OUTPUTS: [1-2 line summary of decisions, file paths, key findings]
   NEXT: Phase N+1 -- [description]
   ```
2. **Carry forward only key outputs**: Pass only essential results (decisions, file paths, key findings) to the next phase -- not the full sub-agent output
3. **If you lose track**: Check your most recent CHECKPOINT output to determine where you are in the workflow
4. **Keep sub-agent prompts focused**: Give each sub-agent only the context it needs, not the entire workflow history

## Execution Rules

1. Phase 1: Steps 1a and 1b run in **parallel**
2. Phase 2: Steps 2a and 2b run in **parallel** (wait for Phase 1)
3. Phase 3: Sequential within phase (wait for Phase 2)
4. Phase 4: Steps 4a, 4b, and 4c run in **parallel** (wait for Phase 3)
5. If any step identifies a blocker, stop and report to user
6. Synthesize all outputs into a final delivery report

## Final Output

```
## Feature Delivery Report

### Feature: [name]
### Status: [Complete / Blocked]

### Deliverables
| Phase | Deliverable | Status |
|-------|------------|--------|
| Requirements | BRD + FSD | Done |
| Architecture | Blueprint + Task Breakdown | Done |
| Tests | Test Suite (xUnit / Vitest / Playwright) | Done |
| Code | .NET solution + React app | Done |
| QA | Test Reports + Code Review | Done |
| Deployment | Deploy Plan (GitHub Actions + Docker) | Done |

### Files Created/Modified
[List all files]

### Next Steps
[Any remaining actions]
```
