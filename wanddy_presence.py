#!/usr/bin/env python3
"""
Wanddy Discord gateway presence client.

Maintains a WebSocket connection to Discord so the bot avatar shows ONLINE
(green dot) and a custom activity ("Watching · 18 agents") in the member list.

Uses intents=0 (no privileged intents required for plain presence).

Run: DISCORD_TOKEN=... python3 wanddy_presence.py
Or use the .env file's token (loaded automatically if present).
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

try:
    import websockets
except ImportError:
    print("websockets package missing. Install: pip3 install websockets", file=sys.stderr)
    sys.exit(2)

GATEWAY_URL = "wss://gateway.discord.gg/?v=10&encoding=json"
INTENTS = 0  # No privileged intents needed for presence

load_dotenv(Path(__file__).resolve().parent / ".env")
TOKEN = os.environ.get("DISCORD_TOKEN")

if not TOKEN:
    print("DISCORD_TOKEN not set", file=sys.stderr)
    sys.exit(2)


async def heartbeat_loop(ws, interval_ms: float, last_seq_ref: list):
    while True:
        await asyncio.sleep(interval_ms / 1000)
        try:
            await ws.send(json.dumps({"op": 1, "d": last_seq_ref[0]}))
        except websockets.ConnectionClosed:
            return


async def run_once():
    last_seq = [None]
    async with websockets.connect(GATEWAY_URL, max_size=2**20) as ws:
        hello = json.loads(await ws.recv())
        if hello.get("op") != 10:
            print(f"[{time.strftime('%H:%M:%S')}] Unexpected first frame: {hello}", file=sys.stderr)
            return
        interval = hello["d"]["heartbeat_interval"]
        identify = {
            "op": 2,
            "d": {
                "token": TOKEN,
                "intents": INTENTS,
                "properties": {
                    "os": "linux",
                    "browser": "wanddy-presence",
                    "device": "wanddy-presence",
                },
                "presence": {
                    "activities": [{"name": "Watching · 18 agents", "type": 3}],
                    "status": "online",
                    "afk": False,
                },
            },
        }
        await ws.send(json.dumps(identify))
        hb_task = asyncio.create_task(heartbeat_loop(ws, interval, last_seq))
        try:
            async for raw in ws:
                msg = json.loads(raw)
                if "s" in msg and msg["s"] is not None:
                    last_seq[0] = msg["s"]
                t = msg.get("t")
                op = msg.get("op")
                if t == "READY":
                    user = msg["d"].get("user", {})
                    print(f"[{time.strftime('%H:%M:%S')}] READY — connected as {user.get('username')}#{user.get('discriminator')} (bot is now ONLINE)", flush=True)
                elif op == 7:  # Reconnect
                    print(f"[{time.strftime('%H:%M:%S')}] Gateway requested reconnect", flush=True)
                    return
                elif op == 9:  # Invalid session
                    print(f"[{time.strftime('%H:%M:%S')}] Invalid session — exiting", flush=True)
                    sys.exit(3)
        finally:
            hb_task.cancel()


async def main():
    while True:
        try:
            await run_once()
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Connection error: {e}; retrying in 5s", flush=True)
        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
