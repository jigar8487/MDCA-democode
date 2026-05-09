#!/bin/bash
# Claude Code Pre-Review Hook
# Runs before code review to catch common issues on the .NET 9 + React 18 stack.

# Color codes
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

EXIT_CODE=0

# Check for hardcoded credentials in staged files (skip docs and settings)
if git diff --cached --name-only 2>/dev/null \
    | xargs grep -l -E "(api_key|api_secret|password|access_token|connection_string)\s*=\s*['\"][^'\"]+['\"]" 2>/dev/null \
    | grep -v "\.md$" | grep -v "\.yml$" | grep -v "appsettings\.Development\.json$"; then
    echo -e "${RED}BLOCKED: Possible hardcoded credentials found in staged files${NC}" >&2
    EXIT_CODE=2
fi

# Check for Console.WriteLine in C# (use ILogger / Serilog instead)
CS_PRINT=$(git diff --cached --name-only -- "*.cs" 2>/dev/null \
    | xargs grep -l -E "Console\.(Write|WriteLine)\(" 2>/dev/null \
    | grep -v "/Tests/" | grep -v "Program\.cs$")
if [ -n "$CS_PRINT" ]; then
    echo -e "${YELLOW}WARNING: Console.WriteLine in C# files (use ILogger / Serilog instead):${NC}" >&2
    echo "$CS_PRINT" >&2
fi

# Check for console.log in TS/TSX files (should be removed before merge)
TS_LOG=$(git diff --cached --name-only -- "*.ts" "*.tsx" 2>/dev/null \
    | xargs grep -l -E "console\.(log|debug)\(" 2>/dev/null \
    | grep -v "\.test\." | grep -v "/__tests__/")
if [ -n "$TS_LOG" ]; then
    echo -e "${YELLOW}WARNING: console.log/debug in production TS/TSX (remove before merge):${NC}" >&2
    echo "$TS_LOG" >&2
fi

# Check for raw SQL string interpolation in C# (injection risk)
SQL_INJECTION=$(git diff --cached -- "*.cs" 2>/dev/null \
    | grep -E "^\+.*(FromSqlRaw|ExecuteSqlRaw)\(.*\\\$\"" )
if [ -n "$SQL_INJECTION" ]; then
    echo -e "${RED}BLOCKED: Possible SQL injection — use FromSqlInterpolated / parameterized queries${NC}" >&2
    EXIT_CODE=2
fi

# Detect new EF Core migrations and warn to verify Up/Down + Designer file are staged together
NEW_MIGRATIONS=$(git diff --cached --name-only -- "*Migrations/*.cs" 2>/dev/null \
    | grep -v "Designer\.cs$" | grep -v "ModelSnapshot\.cs$")
if [ -n "$NEW_MIGRATIONS" ]; then
    echo -e "${YELLOW}INFO: EF Core migration changes detected — verify Designer.cs and ModelSnapshot.cs are staged together:${NC}" >&2
    echo "$NEW_MIGRATIONS" >&2
fi

# Detect new public APIs in controllers without [Authorize] (heuristic)
UNAUTH_ENDPOINTS=$(git diff --cached -- "*Controller.cs" 2>/dev/null \
    | grep -B1 -E "^\+.*\[Http(Get|Post|Put|Delete|Patch)\]" \
    | grep -v "Authorize" | grep -v "AllowAnonymous" | grep -E "^\+.*Http")
if [ -n "$UNAUTH_ENDPOINTS" ]; then
    echo -e "${YELLOW}INFO: New HTTP endpoints detected — verify [Authorize] or [AllowAnonymous] is explicit on each${NC}" >&2
fi

exit $EXIT_CODE
