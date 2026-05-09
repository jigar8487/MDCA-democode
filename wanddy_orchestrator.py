"""
Wanddy orchestrator — one cron iteration, fully Langfuse-traced.

Replaces the ad-hoc curl/MCP orchestration with a Python program so every
Discord-driven request produces a real trace tree:

  iteration (agent span)
    ├─ scan-discord            (span)        — list channel + threads
    ├─ for each new message:
    │     handle-new-message   (agent span)
    │       ├─ create-thread   (tool span)
    │       ├─ post-ack        (tool span)
    │       ├─ wanddy-planner  (agent span — calls openrouter, auto-traced)
    │       ├─ post-plan       (tool span)
    │       └─ create-jira     (tool span)
    └─ for each thread reply:
          handle-thread-reply  (agent span)
            ├─ classify-reply  (span)
            └─ on approve:     execute-plan (agent span)

State file: .claude/agent-bus/orchestrator_state.json — maps Discord
message IDs to {thread, jira_key, status, last_handled_msg_id} so we
don't reprocess.

Run once (e.g. from a cron tick):
    python3 wanddy_orchestrator.py
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Any

import requests

from agents import agent_act, read_files
from langfuse import propagate_attributes
from langfuse_setup import assert_credentials_ok, langfuse
from wanddy_planner import plan_request


# --- Config (filled by _init_orchestrator_config from environment) ------------
ORCHESTRATOR_CHANNEL_ID: str = ""
JIRA_CLOUD_ID: str = ""
JIRA_PROJECT_KEY: str = ""
JIRA_BASE: str = ""
JIRA_BROWSE_BASE_URL: str = ""
DISCORD_BASE = "https://discord.com/api/v10"

STATE_PATH = Path(__file__).parent / ".claude" / "agent-bus" / "orchestrator_state.json"

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    print("DISCORD_TOKEN missing", file=sys.stderr)
    sys.exit(2)

DISCORD_HEADERS = {
    "Authorization": f"Bot {DISCORD_TOKEN}",
    "Content-Type": "application/json",
}


def _init_orchestrator_config() -> None:
    """Load Discord/Jira identifiers from the environment. Exits on missing keys."""
    global ORCHESTRATOR_CHANNEL_ID, JIRA_CLOUD_ID, JIRA_PROJECT_KEY, JIRA_BASE, JIRA_BROWSE_BASE_URL
    required = (
        "DISCORD_ORCHESTRATOR_CHANNEL_ID",
        "JIRA_CLOUD_ID",
        "JIRA_PROJECT_KEY",
        "JIRA_BROWSE_BASE_URL",
    )
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        print(
            "Missing required environment variables: " + ", ".join(missing),
            file=sys.stderr,
        )
        sys.exit(2)
    ORCHESTRATOR_CHANNEL_ID = os.environ["DISCORD_ORCHESTRATOR_CHANNEL_ID"]
    JIRA_CLOUD_ID = os.environ["JIRA_CLOUD_ID"]
    JIRA_PROJECT_KEY = os.environ["JIRA_PROJECT_KEY"]
    JIRA_BROWSE_BASE_URL = os.environ["JIRA_BROWSE_BASE_URL"].rstrip("/")
    JIRA_BASE = f"https://api.atlassian.com/ex/jira/{JIRA_CLOUD_ID}/rest/api/3"


_init_orchestrator_config()


# --- State ------------------------------------------------------------------
def load_state() -> dict[str, Any]:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"processed_messages": {}}


def save_state(state: dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2))


# --- Discord I/O (each wrapped in a span via the caller) --------------------
def discord_get(path: str) -> Any:
    r = requests.get(f"{DISCORD_BASE}{path}", headers=DISCORD_HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()


def discord_post(path: str, body: dict[str, Any]) -> Any:
    r = requests.post(
        f"{DISCORD_BASE}{path}", headers=DISCORD_HEADERS, json=body, timeout=15
    )
    r.raise_for_status()
    return r.json() if r.text else {}


def discord_put(path: str) -> int:
    r = requests.put(f"{DISCORD_BASE}{path}", headers=DISCORD_HEADERS, timeout=15)
    return r.status_code


def fire_typing(channel_id: str) -> None:
    requests.post(
        f"{DISCORD_BASE}/channels/{channel_id}/typing",
        headers=DISCORD_HEADERS,
        timeout=10,
    )


# --- Jira I/O ---------------------------------------------------------------
def jira_request(method: str, path: str, body: dict | None = None) -> Any:
    """Direct Atlassian REST call. Reuses Atlassian OAuth via the user's cli
    only if available; otherwise this returns 401 and the orchestrator
    surfaces a graceful error. The MCP-bound credentials in this Claude
    session aren't reachable from a separate Python process — but the
    Discord+Langfuse half of the orchestrator is fully wired up. To enable
    Jira writes, add ATLASSIAN_API_TOKEN + ATLASSIAN_EMAIL to .env (basic auth).
    """
    auth = None
    email = os.environ.get("ATLASSIAN_EMAIL")
    token = os.environ.get("ATLASSIAN_API_TOKEN")
    if email and token:
        auth = (email, token)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    url = f"{JIRA_BASE}{path}"
    r = requests.request(
        method, url, headers=headers, auth=auth, json=body, timeout=15
    )
    return r.status_code, (r.json() if r.text else {})


def create_jira_placeholder(user_message: str, source_msg_id: str) -> dict:
    status, body = jira_request(
        "POST",
        "/issue",
        {
            "fields": {
                "project": {"key": JIRA_PROJECT_KEY},
                "issuetype": {"name": "Task"},
                "summary": f"Wanddy-PLACEHOLDER-{user_message[:80]}",
                "description": (
                    f"Discord source: msg `{source_msg_id}`\n\n"
                    f"> {user_message}\n\nRouted to Planner. v2 workflow."
                ),
            }
        },
    )
    return {"status": status, "body": body}


# --- Orchestrator pipeline (each step is a span) ----------------------------
def scan_discord(state: dict) -> dict[str, Any]:
    """Returns {new_messages: [...], thread_replies: [...]}"""
    with langfuse.start_as_current_observation(
        as_type="tool", name="scan-discord", input={"channel": ORCHESTRATOR_CHANNEL_ID}
    ) as span:
        msgs = discord_get(f"/channels/{ORCHESTRATOR_CHANNEL_ID}/messages?limit=20")
        new_messages = []
        for m in msgs:
            if m["author"].get("bot"):
                continue
            if m.get("thread"):
                continue  # already threaded — handled by reply check
            if any(r.get("emoji", {}).get("name") == "✅" for r in m.get("reactions", [])):
                continue
            if m["id"] in state["processed_messages"]:
                continue
            new_messages.append(m)

        thread_replies = []
        for msg_id, info in state["processed_messages"].items():
            thread_id = info.get("thread_id")
            if not thread_id or info.get("status") == "rejected":
                continue
            # NOTE: previously skipped status=='done', which silently dropped
            # follow-up questions in completed threads. Now we handle replies
            # in done threads as "follow-up" — they get a brief Wanddy ack
            # plus an optional re-route, but won't re-trigger the agent chain.
            try:
                thr_msgs = discord_get(f"/channels/{thread_id}/messages?limit=5")
            except Exception:
                continue
            thr_msgs.sort(key=lambda x: x["id"])
            last_user_reply = None
            last_handled = info.get("last_handled_reply_id")
            last_handled_int = int(last_handled) if last_handled else 0
            for tm in reversed(thr_msgs):
                if tm["author"].get("bot"):
                    continue
                # Discord snowflake IDs are monotonically increasing — anything
                # with id <= last_handled is already processed (or older than it).
                if int(tm["id"]) <= last_handled_int:
                    break
                last_user_reply = tm
                break
            if last_user_reply:
                thread_replies.append(
                    {"msg_id": msg_id, "thread_id": thread_id, "reply": last_user_reply}
                )

        result = {
            "new_count": len(new_messages),
            "reply_count": len(thread_replies),
        }
        span.update(output=result)
        return {
            "new_messages": new_messages,
            "thread_replies": thread_replies,
            "summary": result,
        }


def handle_new_message(msg: dict, state: dict) -> None:
    user_message = msg["content"]
    user_id = msg["author"]["id"]
    msg_id = msg["id"]

    with propagate_attributes(
        trace_name="wanddy-orchestration",
        user_id=user_id,
        session_id=msg_id,
        tags=["surface:wanddy-orchestrator", "phase:new-message"],
        metadata={
            "discord_msg_id": msg_id,
            "discord_channel_id": ORCHESTRATOR_CHANNEL_ID,
        },
    ), langfuse.start_as_current_observation(
        as_type="agent",
        name="handle-new-message",
        input={"user_message": user_message, "user_id": user_id, "msg_id": msg_id},
    ) as outer:

        # 1. typing + thread
        with langfuse.start_as_current_observation(
            as_type="tool", name="create-thread", input={"msg_id": msg_id}
        ) as s:
            fire_typing(ORCHESTRATOR_CHANNEL_ID)
            short = user_message[:60].replace("\n", " ")
            thr = discord_post(
                f"/channels/{ORCHESTRATOR_CHANNEL_ID}/messages/{msg_id}/threads",
                {"name": f"TASK: {short}", "auto_archive_duration": 1440},
            )
            thread_id = thr["id"]
            s.update(output={"thread_id": thread_id})

        # 2. ack
        with langfuse.start_as_current_observation(
            as_type="tool", name="post-ack", input={"thread_id": thread_id}
        ) as s:
            fire_typing(thread_id)
            discord_post(
                f"/channels/{thread_id}/messages",
                {
                    "content": (
                        f"**[Wanddy]** Request received from <@{user_id}>: "
                        f"*\"{user_message[:200]}\"*.\n\nCreating Jira placeholder "
                        "and routing to **Planner Agent**."
                    )
                },
            )
            s.update(output={"posted": True})

        # 3. Jira placeholder
        with langfuse.start_as_current_observation(
            as_type="tool", name="create-jira", input={"summary": user_message[:80]}
        ) as s:
            jira = create_jira_placeholder(user_message, msg_id)
            jira_key = (jira.get("body") or {}).get("key")
            s.update(output={"status": jira["status"], "key": jira_key})

        # 4. plan via traced planner (wanddy-planner observation already nests here)
        plan_result = plan_request(
            user_message=user_message,
            discord_user_id=user_id,
            discord_thread_id=thread_id,
        )
        plan_text = plan_result["plan_text"]

        # 5. post plan
        with langfuse.start_as_current_observation(
            as_type="tool", name="post-plan", input={"thread_id": thread_id}
        ) as s:
            fire_typing(thread_id)
            if jira_key:
                preface = (
                    f"**[Wanddy → Planner Agent]** Plan for [{jira_key}]"
                    f"({JIRA_BROWSE_BASE_URL}/{jira_key}):\n\n"
                )
            else:
                preface = "**[Wanddy → Planner Agent]** Plan:\n\n"
            content = preface + plan_text + "\n\nReply: **approve** / **modify** / **reject**"
            if len(content) > 1900:
                content = content[:1900] + "..."
            discord_post(f"/channels/{thread_id}/messages", {"content": content})
            s.update(output={"posted": True, "len": len(content)})

        # 6. record state
        state["processed_messages"][msg_id] = {
            "thread_id": thread_id,
            "jira_key": jira_key,
            "status": "awaiting-approval",
            "request": user_message,
            "user_id": user_id,
            "plan_trace_id": plan_result.get("trace_id"),
            "ts": int(time.time()),
        }
        outer.update(
            output={
                "thread_id": thread_id,
                "jira_key": jira_key,
                "plan_trace_id": plan_result.get("trace_id"),
            }
        )


def classify_reply(reply_text: str) -> str:
    t = reply_text.strip().lower()
    if any(k in t for k in ["approve", "yes", "go ahead", "proceed", "ok"]):
        return "approve"
    if any(k in t for k in ["reject", "cancel", "no"]):
        return "reject"
    return "modify"


def handle_thread_reply(item: dict, state: dict) -> None:
    msg_id = item["msg_id"]
    thread_id = item["thread_id"]
    reply = item["reply"]
    info = state["processed_messages"][msg_id]
    is_done_thread = info.get("status") == "done"

    with propagate_attributes(
        trace_name="wanddy-orchestration",
        user_id=info["user_id"],
        session_id=msg_id,
        tags=[
            "surface:wanddy-orchestrator",
            "phase:thread-reply" if not is_done_thread else "phase:follow-up",
        ],
        metadata={
            "discord_msg_id": msg_id,
            "thread_id": thread_id,
            "jira_key": info.get("jira_key") or "",
        },
    ), langfuse.start_as_current_observation(
        as_type="agent",
        name="handle-thread-reply",
        input={"reply_text": reply["content"][:200], "is_follow_up": is_done_thread},
    ) as outer:
        # Follow-up on a done thread: ack briefly, suggest opening a fresh
        # request in the channel for new work. Don't re-run the agent chain.
        if is_done_thread:
            with langfuse.start_as_current_observation(
                as_type="tool", name="post-followup-ack",
                input={"thread_id": thread_id, "reply": reply["content"][:120]},
            ) as s:
                fire_typing(thread_id)
                ack = (
                    "**[Wanddy]** Got your follow-up on this completed task. "
                    f"For new work or extensions to **{info.get('jira_key') or 'this task'}**, "
                    f"please post a fresh message in <#{ORCHESTRATOR_CHANNEL_ID}> — orchestrator "
                    "will pick it up within ~1 min and run the full traced flow. 🟢 alive."
                )
                discord_post(f"/channels/{thread_id}/messages", {"content": ack})
                s.update(output={"posted": True})
            info["last_handled_reply_id"] = reply["id"]
            outer.update(output={"decision": "follow-up-ack"})
            return

        with langfuse.start_as_current_observation(
            as_type="span", name="classify-reply", input={"text": reply["content"][:120]}
        ) as s:
            decision = classify_reply(reply["content"])
            s.update(output={"decision": decision})

        with langfuse.start_as_current_observation(
            as_type="tool", name="post-decision", input={"decision": decision}
        ) as s:
            fire_typing(thread_id)
            if decision == "approve":
                msg = "**[Wanddy]** Plan approved ✅. Routing to agents (sequential)..."
            elif decision == "reject":
                msg = "**[Wanddy]** Task cancelled ❌."
                info["status"] = "rejected"
            else:
                msg = "**[Wanddy]** Got your feedback — marking as needs-modify."
                info["status"] = "modify-requested"
            discord_post(f"/channels/{thread_id}/messages", {"content": msg})
            s.update(output={"posted": True})

        # On approve: execute traced agent chain (Aarav -> Jignesh -> Kavya).
        if decision == "approve":
            execute_agent_chain(
                request=info["request"],
                jira_key=info.get("jira_key") or f"{JIRA_PROJECT_KEY}-?",
                thread_id=thread_id,
            )
            info["status"] = "done"

        info["last_handled_reply_id"] = reply["id"]
        outer.update(output={"decision": decision, "new_status": info["status"]})


def execute_agent_chain(request: str, jira_key: str, thread_id: str) -> None:
    """Run Aarav -> Jignesh -> Kavya as real LLM calls. Aarav writes actual
    files to disk; reviewers see the file content in their context. Each call
    is traced as a generation; each Discord post is a tool span."""

    with langfuse.start_as_current_observation(
        as_type="agent",
        name="execute-agent-chain",
        input={"request": request, "jira_key": jira_key},
    ) as outer:
        ctx_base = {"jira_key": jira_key, "request": request}

        # 1. Aarav implements (writes real files)
        aarav = agent_act(
            role="developer-aarav",
            task=f"Implement: {request}",
            context=ctx_base,
        )
        files_written = aarav.get("files_written", [])
        aarav_summary = aarav.get("summary") or aarav["text"][:500]

        with langfuse.start_as_current_observation(
            as_type="tool", name="post-agent-msg",
            input={"role": "developer-aarav", "thread_id": thread_id, "files": files_written},
        ) as s:
            fire_typing(thread_id)
            files_line = (
                "\n📁 Files written: " + ", ".join(f"`{p}`" for p in files_written)
                if files_written else "\n⚠️  No files written (LLM didn't return valid file envelope)"
            )
            pretty = f"**[developer-aarav]**\n{aarav_summary[:1500]}{files_line}"
            if len(pretty) > 1900:
                pretty = pretty[:1900] + "..."
            discord_post(f"/channels/{thread_id}/messages", {"content": pretty})
            s.update(output={"posted": True, "files": files_written})

        # 2. Jignesh reviews — reads the actual files
        file_contents = read_files(files_written) if files_written else {}
        ctx_review = {**ctx_base, "files": file_contents, "files_written": files_written}
        jignesh = agent_act(
            role="tech-lead-jignesh",
            task=f"Review what Aarav delivered for: {request}",
            context=ctx_review,
        )
        with langfuse.start_as_current_observation(
            as_type="tool", name="post-agent-msg",
            input={"role": "tech-lead-jignesh", "thread_id": thread_id},
        ) as s:
            fire_typing(thread_id)
            pretty = f"**[tech-lead-jignesh]**\n{jignesh['text'][:1700]}"
            if len(pretty) > 1900:
                pretty = pretty[:1900] + "..."
            discord_post(f"/channels/{thread_id}/messages", {"content": pretty})
            s.update(output={"posted": True})

        # 3. Kavya validates — also sees the files + Jignesh's review
        ctx_qa = {
            **ctx_base,
            "files": file_contents,
            "files_written": files_written,
            "tech_lead_review": jignesh["text"][:800],
        }
        kavya = agent_act(
            role="manual-qa-kavya",
            task=f"Validate the implementation + review for: {request}",
            context=ctx_qa,
        )
        with langfuse.start_as_current_observation(
            as_type="tool", name="post-agent-msg",
            input={"role": "manual-qa-kavya", "thread_id": thread_id},
        ) as s:
            fire_typing(thread_id)
            pretty = f"**[manual-qa-kavya]**\n{kavya['text'][:1700]}"
            if len(pretty) > 1900:
                pretty = pretty[:1900] + "..."
            discord_post(f"/channels/{thread_id}/messages", {"content": pretty})
            s.update(output={"posted": True})

        outer.update(
            output={
                "chain_complete": True,
                "files_written": files_written,
                "agents_run": ["developer-aarav", "tech-lead-jignesh", "manual-qa-kavya"],
            }
        )


def main() -> int:
    assert_credentials_ok()
    state = load_state()

    with langfuse.start_as_current_observation(
        as_type="agent",
        name="wanddy-orchestration-iteration",
        input={"channel": ORCHESTRATOR_CHANNEL_ID, "tracked_msgs": len(state["processed_messages"])},
    ) as iter_span:
        scan = scan_discord(state)

        for msg in scan["new_messages"]:
            try:
                handle_new_message(msg, state)
            except Exception as e:
                print(f"[orchestrator] error on new msg {msg.get('id')}: {e}", file=sys.stderr)

        for item in scan["thread_replies"]:
            try:
                handle_thread_reply(item, state)
            except Exception as e:
                print(f"[orchestrator] error on reply {item.get('msg_id')}: {e}", file=sys.stderr)

        save_state(state)
        iter_span.update(
            output={
                "new_handled": scan["summary"]["new_count"],
                "replies_handled": scan["summary"]["reply_count"],
                "tracked_total": len(state["processed_messages"]),
            }
        )
        trace_id = langfuse.get_current_trace_id()
        trace_url = langfuse.get_trace_url(trace_id=trace_id) if trace_id else None

    langfuse.flush()
    print(f"new_handled={scan['summary']['new_count']} replies_handled={scan['summary']['reply_count']}")
    print(f"trace_url={trace_url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
