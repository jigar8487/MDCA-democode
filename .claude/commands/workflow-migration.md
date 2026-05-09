# Workflow: Version Migration

You are orchestrating a migration for the .NET + React project. This workflow covers BOTH:
- (a) **.NET version upgrade** (e.g., .NET 6 -> .NET 9, React 17 -> React 18) on an existing project, AND
- (b) **Legacy modernization** of a non-.NET / older system to the .NET 9 + React 18 + TypeScript stack on Linux/Docker.

**Migration Request**: "$ARGUMENTS"

---

## Phase 1: Assessment (Parallel)

### Step 1a: Architecture Review (`/hiren`)
- Review compatibility with target .NET version (target framework moniker, breaking changes in ASP.NET Core, EF Core, runtime APIs)
- Identify deprecated APIs, removed packages, NuGet upgrades required
- Assess React 18 migration needs (concurrent rendering, automatic batching, Suspense behavior, Strict Mode, deprecated lifecycles, TypeScript version bumps)
- For legacy modernization: define target architecture (clean architecture: Api / Domain / Application / Infrastructure / Web), data model migration to EF Core + PostgreSQL, UI rewrite to React 18 + TypeScript
- Output: Migration compatibility report

### Step 1b: Sequencing + Risk (`/jignesh`)
- Create per-solution / per-project migration schedule and PR sequencing
- Estimate effort per .NET project and React module
- Define rollback strategy (Docker image rollback, EF migration rollback, feature flags / strangler pattern for legacy modernization)
- Output: Migration sequencing + rollback plan

---

## Phase 2: Migration (Sequential per project / module)

### Step 2: Code Migration (`/jignesh` -> `/aarav`)
For each project / module:
- `/jignesh`: Identify specific changes needed (.csproj target framework, NuGet upgrades, package.json deps, deprecated API replacements, namespace renames)
- `/aarav`: Update code — bump TFM in `.csproj`, run `dotnet outdated` / `npm outdated`, fix deprecated APIs, migrate React class components to functional components / new hooks where required, run dry-run `dotnet build` and `dotnet ef database update --dry-run` until clean
- For legacy modernization: port modules into new clean-architecture projects, replace ORM with EF Core, replace UI with React TSX components
- Output: Migrated project / module code

### Step 3: Integration Updates (`/yash`)
- Update integration code for new framework version (HttpClient, Polly, message bus client APIs)
- Update authentication libraries (JWT, OAuth, OpenIdConnect)
- Output: Updated integration code

---

## Phase 3: Validation (Parallel)

### Step 4a: Automated Testing (`/riya`)
- Run existing test suite on new framework version (xUnit, Vitest, Playwright)
- Fix failing tests caused by framework changes
- Add new tests for migration-specific changes
- Output: Test results

### Step 4b: Functional Validation (`/kavya`)
- Manual testing of all critical flows post-migration
- Validate business processes still behave correctly on the upgraded stack
- Output: Validation report

---

## Phase 4: Deployment (Cutover)

### Step 5: Staging Deploy (`/tejas`)
- Build new Docker image targeting upgraded .NET / React, push to GHCR
- Deploy to staging via GitHub Actions
- Apply EF Core migrations
- Output: Staging deployment status

### Step 6: Cutover + Rollback Readiness (`/tejas`)
- Plan production cutover window
- Confirm `pg_dump` backup + container volume snapshot taken before cutover
- Confirm rollback path: previous Docker image tag + `dotnet ef migrations script --idempotent` reverse script ready
- Output: Cutover + rollback plan

### Step 7: Post-Migration Support (`/bhavin`)
- Prepare client communication
- Document known behavior changes between versions
- Output: Migration support plan

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

1. Phase 1 runs in parallel
2. Phase 2 is sequential (project by project / module by module)
3. Phase 3 runs in parallel
4. Phase 4 is sequential
5. Each project must pass tests before moving to the next
6. **MUST get user confirmation** before production cutover (Step 6)

## Final Output

```
## Migration Report

### Migration: [.NET source -> target] / [Legacy stack -> .NET 9 + React 18]
### Status: [Complete / In Progress / Blocked]

### Project Status
| Project / Module | Status | Changes | Tests |
|------------------|--------|---------|-------|

### Breaking Changes
| Change | Affected Projects | Resolution |
|--------|-------------------|------------|

### Risk Assessment
| Risk | Severity | Mitigation |
|------|----------|------------|

### Rollback Plan
| Step | Owner | Status |
|------|-------|--------|
```
