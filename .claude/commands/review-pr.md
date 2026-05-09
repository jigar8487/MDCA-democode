# Review Pull Request

Review the current branch's changes against the base branch for the .NET + React project (.NET 9 + React 18 + TypeScript on Linux/Docker).

**PR/Branch**: "$ARGUMENTS"

If no argument given, review the current branch's diff against `develop`.

---

## Instructions

1. **Identify changes**: Run `git diff develop...HEAD --stat` to see all changed files. If a specific PR number is given, run `gh pr diff <number>` instead.

2. **Read all changed files** completely. Do not skip any file.

3. **Review against REVIEW.md**: Read `/REVIEW.md` for the project's review standards.

4. **Perform the review** across these dimensions:

### Architecture Review
- Clean architecture boundaries respected (Domain has no Infrastructure refs, Application depends on Domain, Web/Api depends on Application)
- Proper use of repository / service / DI registration
- DbContext + `DbSet<TEntity>` definitions, EF Core fluent configuration in `OnModelCreating` or `IEntityTypeConfiguration<T>`
- `[ApiController]` + attribute routing on controllers; minimal API endpoints grouped properly
- `IOptions<T>` / `IOptionsSnapshot<T>` for configuration binding
- Async all the way; cancellation tokens flowed through
- React: functional components with hooks (no class components), TypeScript strict, prop types defined

### Security Review
- ASP.NET Core authorization policies / `[Authorize]` attributes for ALL non-public endpoints
- No hardcoded API keys, passwords, or secrets in source / appsettings (use user-secrets, env vars, Key Vault)
- Parameterized queries / EF Core LINQ only (no string interpolation in `FromSqlRaw`)
- Tenant / multi-company isolation via global query filters
- HMAC verification on inbound webhook endpoints
- React: no `dangerouslySetInnerHTML` on user-controlled data, CSRF tokens for cookie auth, secure cookie flags

### External-System Integration Review (if applicable)
- Typed `HttpClient` via `IHttpClientFactory`, Polly for retry / circuit breaker
- Rate-limit handling (429 backoff)
- Idempotent import operations (idempotency keys, upsert semantics)
- External-id mapping persisted for synced records
- Cancellation + timeouts honored

### Data Operations Review (merges, dedup, financial) (if applicable)
- Operation wrapped in EF Core transaction / savepoint
- All reassignments logged in audit table
- Reconciliation verified post-operation
- Cross-tenant records not auto-merged
- Rollback restores ALL records to original state

### Code Quality
- Methods under 50 lines
- Early returns over nested conditionals
- Serilog structured logging (no `Console.WriteLine`)
- XML doc comments on public APIs
- `base.X()` called in all lifecycle overrides where required
- No N+1 query patterns

### Test Coverage
- New entities / services have xUnit tests
- API integrations have integration tests (WebApplicationFactory, WireMock.Net)
- Critical flows have Playwright E2E
- React components have Vitest + React Testing Library tests
- Edge cases covered

5. **Output the review** in this exact format:

```
## Code Review Report

### Branch: [branch name]
### Files Changed: [count]
### Overall Verdict: [APPROVED / CHANGES REQUIRED / REJECTED]

---

### CRITICAL Issues (Must Fix Before Merge)
| # | File:Line | Issue | Suggested Fix |
|---|-----------|-------|---------------|

### WARNING Issues (Should Fix)
| # | File:Line | Issue | Suggested Fix |
|---|-----------|-------|---------------|

### SUGGESTIONS (Nice to Have)
| # | File:Line | Suggestion |
|---|-----------|------------|

---

### Architecture: [Compliant / Deviations Found]
[Details if deviations]

### Security: [Clean / Issues Found]
[Details if issues]

### Test Coverage: [Sufficient / Gaps Found]
[Details if gaps]

### Integration Safety: [N/A / Clean / Issues Found]
[Details if applicable]

### Data Operation Safety: [N/A / Clean / Issues Found]
[Details if applicable]
```
