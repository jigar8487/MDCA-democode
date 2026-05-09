# Security Review

Perform a security-focused review on the specified target for the .NET + React project (.NET 9 + React 18 + TypeScript on Linux/Docker). Apply OWASP Top 10 guidance for .NET and React.

**Target**: "$ARGUMENTS"

If no target specified, scan all recently changed files (`git diff develop...HEAD`).

---

## Instructions

1. Identify all files to review (changed files or specified target).
2. Read each file completely.

3. **Check for these security issues:**

### Credential & Secret Leaks
- Hardcoded API keys, passwords, tokens, connection strings
- Secrets in `appsettings.json` (must use user-secrets / env vars / Key Vault)
- Credentials in log statements / Serilog output
- Secrets in comments or XML doc strings
- `.env` files or credential files committed
- GitHub Actions workflow files with inline secrets instead of `${{ secrets.X }}`

### Injection
- **SQL injection**: string interpolation in `FromSqlRaw` / `ExecuteSqlRaw` (use `FromSqlInterpolated` / parameterized queries)
- **Command injection**: `Process.Start` / shell calls with concatenated user input
- **LDAP / NoSQL injection** where applicable
- **Path traversal**: unsanitized file path inputs in static-file or upload handlers

### Authentication & Authorization
- Endpoints without `[Authorize]` or explicit `[AllowAnonymous]` justification
- Missing or overly broad authorization policies
- Tenant / multi-company isolation not enforced (missing global query filters or claims-based scoping)
- JWT validation misconfigured (issuer, audience, signing key, lifetime)
- Cookie auth without `Secure`, `HttpOnly`, `SameSite` flags
- Password storage: not using ASP.NET Core Identity / proper hashing (PBKDF2/Argon2)

### API Security
- Webhook endpoints without HMAC signature verification
- Missing rate limiting (`AddRateLimiter`) on public endpoints
- Sensitive data in API responses (PII, internal IDs, stack traces in `ProblemDetails`)
- Missing input validation (FluentValidation / DataAnnotations)
- Missing CORS configuration or overly permissive (`AllowAnyOrigin` with credentials)
- CSRF protection missing on cookie-authenticated state-changing endpoints
- Insecure deserialization (untrusted JSON / XML / `BinaryFormatter`)

### React / Frontend Security
- `dangerouslySetInnerHTML` on user-controlled data (XSS risk)
- Storing tokens in `localStorage` for high-risk apps (consider HttpOnly cookies)
- Missing CSP headers from backend
- Open redirect via unvalidated URL query params
- Inline `eval` / `new Function` on dynamic strings

### Data Safety
- Destructive operations (delete, merge, bulk update) without transaction / savepoint
- Financial operations without balance verification
- Missing rollback capability on destructive operations
- Cross-tenant data leakage (missing scope filter)
- Logging PII / payment data

### Infrastructure & Supply Chain
- Outdated NuGet / npm packages with known CVEs (`dotnet list package --vulnerable`, `npm audit`)
- Docker base images not pinned to digest / using `latest`
- Nginx config exposing internal endpoints, missing TLS, weak ciphers
- GitHub Actions using non-pinned third-party actions (`uses: someone/x@main`)

4. **Output format:**

```
## Security Review Report

### Target: [files reviewed]
### Overall: [SECURE / ISSUES FOUND / CRITICAL VULNERABILITIES]

### Critical Vulnerabilities
| # | File:Line | Type | Description | Fix |
|---|-----------|------|-------------|-----|

### Security Warnings
| # | File:Line | Type | Description | Fix |
|---|-----------|------|-------------|-----|

### Recommendations
| # | Area | Recommendation |
|---|------|----------------|
```
