# Review File

Perform a focused code review on a specific file or project for the .NET + React stack (.NET 9 + React 18 + TypeScript).

**Target**: "$ARGUMENTS"

---

## Instructions

1. Read the target file(s) completely.
2. Read `REVIEW.md` for review standards.
3. If a project or folder name is given (e.g., `App.Api`, `src/Web/features/customers`), review ALL relevant `.cs` / `.ts` / `.tsx` files in that folder.
4. If a file path is given, review that specific file.

5. Check for:
   - .NET 9 + React 18 architecture compliance (clean architecture boundaries: Api / Domain / Application / Infrastructure / Web)
   - Security issues (ASP.NET Core authorization policies, SQL injection on raw queries, secrets in source / appsettings, unsafe deserialization, XSS via `dangerouslySetInnerHTML`)
   - Code quality (method length, naming, async/await + cancellation tokens, structured logging via Serilog, TypeScript strict mode, no `any`)
   - Missing `base.OnXxx()` calls in lifecycle / framework overrides
   - EF Core N+1 query patterns (missing `.Include` / `AsSplitQuery`, lazy loading misuse)
   - Proper error handling (no swallowed exceptions, `ProblemDetails` for API errors, React error boundaries)
   - Test coverage gaps (xUnit, Vitest + React Testing Library, Playwright)

6. Output findings categorized as CRITICAL / WARNING / SUGGESTION with exact file:line references.
