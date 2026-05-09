# Workflow: Code Review Pipeline

You are orchestrating a code review for the .NET + React project (.NET 9 + React 18 + TypeScript).

**Review Target**: "$ARGUMENTS"

If no specific file/PR/project is provided, review the current git diff or recently changed files.

---

## Step 1: Code Review (`/jignesh`)
Launch a sub-agent with the `/jignesh` skill to:
- Review code against .NET 9 + React 18 + TypeScript standards
- Check solution/project structure (Api / Domain / Application / Infrastructure / Web), DI registration, controller/service/repository patterns, React component layout
- Validate naming conventions, `using` order, async/await usage, nullable reference types, TypeScript strict mode compliance
- Check for EF Core N+1 queries (missing `.Include` / `AsSplitQuery`), proper `try/catch`, cancellation token propagation, React render performance (memoization, key usage)
- Verify migration-safe patterns (additive EF migrations) and i18n strings
- Output: Detailed code review with findings

## Step 2: Architecture Compliance (`/hiren`)
Launch `/hiren` in parallel to:
- Verify the code aligns with architectural decisions (clean architecture boundaries, dependency direction)
- Check entity relationships, DbContext configuration, value objects, aggregate roots
- Validate database design choices (indexes, constraints, owned types)
- Output: Architecture compliance report

## Step 3: Test Coverage (`/riya`)
Launch `/riya` in parallel to:
- Assess test coverage for the reviewed code (xUnit for backend, Vitest + React Testing Library for frontend, Playwright for E2E)
- Identify untested critical paths
- Suggest test cases if coverage is insufficient
- Output: Test coverage assessment

## Step 4: Security Review (`/jignesh`)
If security-related code is found, launch `/jignesh` to:
- Review ASP.NET Core authorization policies / `[Authorize]` attributes for completeness
- Check tenant / multi-company filtering (global query filters, claims-based scoping)
- Validate any raw-SQL or `FromSqlInterpolated` usage (parameterized queries only)
- Check for XSS in React (avoid `dangerouslySetInnerHTML`), CSRF protection, secrets handling, deserialization safety
- Output: Security review findings

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

1. Steps 1, 2, and 3 run in **parallel**
2. Step 4 runs only if security-relevant code is detected
3. Synthesize all findings into a single review report
4. Categorize findings: Critical / Warning / Suggestion

## Final Output

```
## Code Review Report

### Target: [file/project/PR]
### Overall: [Approved / Changes Required / Rejected]

### Critical Issues (Must Fix)
| # | File:Line | Issue | Fix |
|---|-----------|-------|-----|

### Warnings (Should Fix)
| # | File:Line | Issue | Suggestion |
|---|-----------|-------|------------|

### Suggestions (Nice to Have)
| # | File:Line | Suggestion |
|---|-----------|------------|

### Architecture: [Compliant / Deviations Found]
### Test Coverage: [Sufficient / Gaps Identified]
### Security: [Clean / Issues Found]
```
