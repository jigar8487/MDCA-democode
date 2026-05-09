# Discord Post

Post a message to a project Discord channel.

**Message**: "$ARGUMENTS"

---

## Instructions

1. Parse the argument to determine which channel and what message:
   - If starts with `#deploy` or `#deploy-logs`: post to deploy-logs channel
   - If starts with `#pr` or `#pr-updates`: post to pr-updates channel
   - If starts with `#test` or `#test-results`: post to test-results channel
   - If starts with `#alert` or `#alerts`: post to alerts channel
   - If starts with `#<agent-name>` (any agent listed under "Agent Channel IDs"): post to that agent's feed channel
   - Otherwise: post to wanddy-orchestrator channel

2. Post the message using the Discord bot (token sourced from `$DISCORD_TOKEN` in `.env` — never hardcode):
   ```
   curl -s -X POST "https://discord.com/api/v10/channels/{CHANNEL_ID}/messages" \
     -H "Authorization: Bot ${DISCORD_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{"embeds":[{"description":"...message...","color":3066993}]}'
   ```

## Channel Architecture
- **wanddy-orchestrator** is the ONLY input channel. All user requests/commands land here and are picked up by `/discord-check`.
- All other channels (deploy-logs, pr-updates, test-results, alerts, and every `agent-*` channel) are **output-only / showcase**. Wanddy and the agents post status updates there as work progresses; they do not accept commands.

## Channel IDs

Define snowflakes in your environment (e.g. `.env`); never commit real IDs.

| Channel | Suggested env var |
|---------|-------------------|
| wanddy-orchestrator | `DISCORD_ORCHESTRATOR_CHANNEL_ID` |
| deploy-logs | `DISCORD_DEPLOY_LOGS_CHANNEL_ID` |
| pr-updates | `DISCORD_PR_UPDATES_CHANNEL_ID` |
| test-results | `DISCORD_TEST_RESULTS_CHANNEL_ID` |
| alerts | `DISCORD_ALERTS_CHANNEL_ID` |

## Agent Channel IDs (showcase feeds — output only)

Category snowflake: `DISCORD_AGENTS_CATEGORY_ID` (optional).

| Agent skill | Suggested env var |
|-------------|---------------------|
| developer-aarav | `DISCORD_CHANNEL_DEVELOPER_AARAV` |
| devops-tejas | `DISCORD_CHANNEL_DEVOPS_TEJAS` |
| integration-specialist-yash | `DISCORD_CHANNEL_INTEGRATION_YASH` |
| manual-qa-kavya | `DISCORD_CHANNEL_MANUAL_QA_KAVYA` |
| qa-automation-riya | `DISCORD_CHANNEL_QA_AUTOMATION_RIYA` |
| solution-architect-hiren | `DISCORD_CHANNEL_SOLUTION_ARCHITECT_HIREN` |
| support-consultant-bhavin | `DISCORD_CHANNEL_SUPPORT_BHAVIN` |
| technical-lead-jignesh | `DISCORD_CHANNEL_TECHNICAL_LEAD_JIGNESH` |

## Color Codes
- Success/Info: 3066993 (green)
- Warning: 16776960 (yellow)
- Error: 15158332 (red)
- Purple: 8311585
