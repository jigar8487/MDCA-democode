#!/usr/bin/env bash
# Jira/Discord bridge hooks for Claude Code (optional).
# Default implementations are no-ops so the repo clones cleanly. Replace with
# your own notifications (webhooks, curl to Discord, Jira REST, etc.).
#
# shellcheck shell=bash

set -euo pipefail

hook_on_commit() {
  : # Post-commit: e.g. notify Discord or transition a Jira issue.
}

# Args: PR title, PR URL, branch name (may be empty if gh is unavailable).
hook_on_pr_created() {
  : # PR created: e.g. post to a technical channel.
}

# Args: EF project name (or unknown), connection name (or default).
hook_on_db_migration() {
  : # Database migration: e.g. alert channel with project + connection.
}

# Parses $TOOL_INPUT without GNU grep -P (portable on macOS/Linux).
hook_on_db_migration_from_tool_input() {
  local input="${TOOL_INPUT:-}"
  local project="unknown"
  local conn="default"
  if [[ "${input}" =~ --project[[:space:]]+([^[:space:]]+) ]]; then
    project="${BASH_REMATCH[1]}"
  fi
  if [[ "${input}" =~ --connection[[:space:]]+([^[:space:]]+) ]]; then
    conn="${BASH_REMATCH[1]}"
  fi
  hook_on_db_migration "${project}" "${conn}"
}
