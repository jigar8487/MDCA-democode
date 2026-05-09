# Pre-Merge Review Checklist

Run a comprehensive pre-merge checklist on the current branch before merging to `develop` for the .NET + React project (.NET 9 + React 18 + TypeScript on Linux/Docker).

**Branch/PR**: "$ARGUMENTS"

---

## Instructions

1. Run `git log develop..HEAD --oneline` to see all commits on this branch.
2. Run `git diff develop...HEAD --stat` to see all changed files.
3. Read ALL changed files.
4. Read `REVIEW.md` for review standards.

5. **Execute this checklist:**

### Solution / Project Structure
- [ ] `.csproj` files have correct `<TargetFramework>` (net9.0) and required NuGet refs
- [ ] DI registrations updated for new services / repositories in `Program.cs` / `ServiceCollectionExtensions`
- [ ] EF Core migration generated and reviewed for new entity / schema changes
- [ ] ASP.NET Core authorization policy / `[Authorize]` attributes set for ALL new endpoints
- [ ] React: new components exported from `index.ts`; routes registered

### Code Quality
- [ ] No hardcoded credentials (use user-secrets / env vars / Key Vault)
- [ ] No `Console.WriteLine` (use Serilog structured logging)
- [ ] All overridden lifecycle / framework methods call `base.X()` where required
- [ ] No string-interpolated SQL (LINQ or parameterized `FromSqlInterpolated` only)
- [ ] Methods under 50 lines
- [ ] Proper error handling (no `catch { }` swallowing exceptions; `ProblemDetails` on API errors; React error boundaries)
- [ ] Async / await used end-to-end with cancellation tokens
- [ ] TypeScript strict mode passes; no `any`

### .NET / React Standards
- [ ] Nullable reference types respected (no `!` overrides without justification)
- [ ] EF Core entity configuration via `IEntityTypeConfiguration<T>` or `OnModelCreating`
- [ ] DTOs separate from entities; AutoMapper / manual mapping consistent
- [ ] React: hooks used per rules of hooks; props typed; no inline anonymous components in JSX
- [ ] i18n / translatable strings via resource files / i18n library
- [ ] Computed / derived state memoized appropriately (`useMemo`, `useCallback`)

### Testing
- [ ] New entities / services have xUnit tests
- [ ] Changed logic has test coverage
- [ ] React components have Vitest + React Testing Library tests
- [ ] Critical user flow has Playwright E2E
- [ ] Tests are self-contained (no shared mutable state, no external dependencies)
- [ ] GitHub Actions CI pipeline passes on the branch

### Git Hygiene
- [ ] Commit messages follow convention (`feat(scope): description`, `fix(scope): ...`)
- [ ] No merge commits (rebase preferred)
- [ ] No unrelated changes mixed in
- [ ] No large binary files committed

6. **Output the checklist** with PASS/FAIL/WARN for each item, with details for any failures.

```
## Pre-Merge Checklist

### Branch: [name] -> develop
### Commits: [count]
### Files Changed: [count]
### Verdict: [READY TO MERGE / NEEDS FIXES / BLOCKED]

| # | Check | Status | Details |
|---|-------|--------|---------|
| 1 | Target framework correct | PASS/FAIL | |
| 2 | DI registrations updated | PASS/FAIL | |
| ... | ... | ... | ... |

### Blocking Issues
[List if any]

### Warnings
[List if any]
```
