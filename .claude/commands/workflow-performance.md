# Workflow: Performance Crisis Resolution

You are orchestrating an urgent performance investigation for the .NET + React project (.NET 9 + React 18 + TypeScript on Linux/Docker, Nginx, PostgreSQL).

**Performance Issue**: "$ARGUMENTS"

This is treated as URGENT. Launch parallel investigations immediately.

---

## Step 1: Parallel Investigation

### Agent A: Application Diagnosis (`/bhavin`)
Launch immediately:
- Profile EF Core query timings (enable `LogTo` / SQL log, check for missing `.Include` and N+1 patterns, candidates for `AsSplitQuery` / `AsNoTracking`)
- Profile ASP.NET Core middleware pipeline timings; check Serilog logs for slow endpoints, exception bursts, and lock contention
- Profile React render performance (React DevTools Profiler, wasted renders, large lists missing virtualization, unmemoized components)
- Identify bottleneck endpoints and slow components
- Output: Application diagnosis report

### Agent B: Infrastructure Review (`/tejas`)
Launch in parallel:
- Review Linux server resources via `top` / `htop` / `vmstat` / `iostat` / Grafana (CPU, memory, disk I/O, network)
- Check PostgreSQL: connection pool (Npgsql `MaxPoolSize`), `pg_stat_statements`, slow-query log, missing indexes
- Check Kestrel / ASP.NET Core hosting, thread pool starvation, GC pressure (dotnet-counters, dotnet-trace)
- Review Nginx reverse proxy settings, timeouts, gzip, HTTP/2, upstream pool
- Check Docker container resource limits and node-level throttling
- Output: Infrastructure assessment

---

## Step 2: Root Cause Analysis (`/hiren`)
Using results from Step 1, launch `/hiren` to:
- Identify architectural root causes
- Recommend structural fixes vs quick wins
- Prioritize optimization targets
- Output: Root cause analysis with prioritized fixes

---

## Step 3: Fix Implementation (Parallel)

### Agent C: Code Optimization (`/jignesh` -> `/aarav`)
- Fix EF Core N+1 (add `.Include`, `AsSplitQuery`, projection to DTO)
- Replace tracked reads with `.AsNoTracking()` where appropriate
- Add database indexes (`HasIndex` in `OnModelCreating` + new EF migration)
- Add response caching / `IMemoryCache` / distributed cache where suitable
- React: add `React.memo`, `useMemo`, `useCallback`, code-splitting (`React.lazy`), list virtualization
- Output: Code optimizations

### Agent D: Infrastructure Tuning (`/tejas`)
- Adjust Kestrel thread pool, Npgsql connection pool size
- Tune PostgreSQL config (`shared_buffers`, `work_mem`, `effective_cache_size`)
- Optimize Nginx caching, gzip/brotli, keep-alive
- Adjust Docker container CPU/memory limits
- Output: Infrastructure changes

---

## Step 4: Validation (`/riya`)
- Run performance benchmark tests (k6 / JMeter / Playwright timing assertions)
- Compare before/after metrics
- Output: Performance benchmark report

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

1. Step 1 agents run in **parallel** (URGENT)
2. Step 2 waits for Step 1 results
3. Step 3 agents run in **parallel**
4. Step 4 validates all changes
5. Report resolution to user immediately

## Final Output

```
## Performance Resolution Report

### Issue: [description]
### Severity: [Critical / High / Medium]
### Status: [Resolved / Improved / Ongoing]

### Root Causes
| # | Cause | Type | Impact |
|---|-------|------|--------|

### Fixes Applied
| Fix | Type | Before | After | Improvement |
|-----|------|--------|-------|-------------|

### Metrics
| Metric | Before | After |
|--------|--------|-------|
| p95 response time | [ms] | [ms] |
| EF query count / request | [n] | [n] |
| Memory (working set) | [MB] | [MB] |
| CPU % (avg) | [%] | [%] |
```
