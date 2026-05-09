# Workflow: Integration Development

You are orchestrating an integration between the .NET 9 backend and an external system for the project (ASP.NET Core + EF Core on Linux/Docker).

**Integration Request**: "$ARGUMENTS"

Execute this workflow by launching sub-agents with maximum parallelism. Only wait when a step genuinely depends on a previous step's output.

---

## Phase 1: Architecture (`/hiren`)

Launch `/hiren` to:
- Capture integration requirements (endpoints, data flow, frequency, SLAs) and data mapping between systems (DTOs <-> external schemas)
- Identify authentication (OAuth2 / API key / mTLS) and error-handling needs
- Design integration pattern: REST (HttpClientFactory + Polly), gRPC, webhooks (ASP.NET Core minimal API receiver), or message bus (RabbitMQ / Azure Service Bus)
- Define background sync strategy (Hangfire / Quartz.NET), retry/backoff (Polly), and dead-letter queue handling
- Plan idempotent operations (idempotency keys, upsert via EF Core), conflict resolution
- Output: Integration architecture with mapping + auth contract

---

## Phase 2: Implementation (Sequential — code depends on design)

### Step 2: Integration Development (`/yash`)
Using Phase 1 outputs, launch `/yash` to:
- Implement typed `HttpClient` clients (with Polly resilience), DTO mapping (AutoMapper or manual), sync logic
- Handle authentication, error handling, retry mechanisms (exponential backoff, circuit breaker)
- Build webhook receiver controllers with HMAC signature verification if needed
- Configure message bus consumers/publishers as required
- Output: Integration code

---

## Phase 3: Review + Testing (Parallel)

### Step 3a: Code Review (`/jignesh`)
Launch `/jignesh` to:
- Review integration code quality
- Validate error handling, idempotency, cancellation tokens, async patterns
- Check security (secret storage in user-secrets / Key Vault / environment, input validation, HMAC verification)
- Output: Review results

### Step 3b: Automated Tests (`/riya`)
Launch `/riya` **in parallel** with `/jignesh` to:
- Write integration test cases with mocked external APIs (WireMock.Net / HttpClient handler mocks)
- Error scenario testing (timeouts, 5xx, invalid signatures)
- Output: Automated test results

### Step 3c: Manual Validation (`/kavya`)
Launch `/kavya` **in parallel** with `/jignesh` and `/riya` to:
- End-to-end flow testing with actual / sandbox API
- Edge case validation
- Output: Manual test report

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

1. Phase 1: Architecture from `/hiren`
2. Phase 2: Sequential implementation by `/yash` (wait for Phase 1)
3. Phase 3: Steps 3a, 3b, and 3c run in **parallel** (wait for Phase 2)
4. If external API credentials are needed, ask user

## Final Output

```
## Integration Report

### Integration: [.NET API <-> External System]
### Pattern: [REST / gRPC / Webhook / Message Bus / Scheduled Sync]
### Status: [Complete / Pending Credentials / Blocked]

### Endpoints
| Endpoint | Method | Direction | Purpose |
|----------|--------|-----------|---------|

### Data Mapping
| .NET DTO Field | External Field | Transform |
|----------------|---------------|-----------|

### Files Created
[list]

### Test Results
| Test | Status |
|------|--------|
```
