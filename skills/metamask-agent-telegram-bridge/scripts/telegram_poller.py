"""
Generic long-polling Telegram bridge for an mm-backed agent.

Adapt `call_agent()` to whatever your agent runner actually is — an OpenAI
Agents SDK `Runner.run(...)`, a plain function call, an in-process queue,
whatever's already used by the agent's primary interface. This file is the
transport; it deliberately has no opinion on what's on the other end of
`call_agent()`.

Start this as a background task alongside your agent's normal process
startup (an async framework's lifespan/startup hook, a supervised thread,
etc.) — it is not meant to run as its own separate service.
"""

import asyncio
import logging
import os

import httpx

logger = logging.getLogger("telegram_poller")

_API_BASE = "https://api.telegram.org/bot{token}"
_MAX_MESSAGE_CHARS = 4000  # Telegram's hard cap is 4096; leave headroom.


def _allowed_user_ids() -> set[str]:
    raw = os.environ.get("TELEGRAM_ALLOWED_USER_IDS", "")
    return {s.strip() for s in raw.split(",") if s.strip()}


async def call_agent(chat_id: str, text: str) -> str:
    """Replace with a real call into your agent runner. `chat_id` is a stable
    per-conversation key — use it to key your agent's thread/session state so
    follow-up messages have continuity. Set your gate-bypass context flag
    (see workflows/telegram-bridge.md) for the duration of this call, if your
    agent has one."""
    raise NotImplementedError("wire this up to your agent runner")


async def _send_message(client: httpx.AsyncClient, api: str, chat_id: int, text: str) -> None:
    url = f"{api}/sendMessage"
    for i in range(0, len(text), _MAX_MESSAGE_CHARS):
        chunk = text[i : i + _MAX_MESSAGE_CHARS]
        resp = await client.post(url, json={"chat_id": chat_id, "text": chunk})
        if resp.status_code != 200:
            logger.error("sendMessage failed: %s %s", resp.status_code, resp.text[:300])


async def run_telegram_poller() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.warning("TELEGRAM_BOT_TOKEN not set — Telegram poller disabled")
        return
    allowed = _allowed_user_ids()
    if not allowed:
        logger.warning(
            "TELEGRAM_ALLOWED_USER_IDS not set — poller disabled "
            "(fail-closed: this bridge never defaults to open-to-anyone)"
        )
        return

    api = _API_BASE.format(token=token)
    offset = 0
    logger.info("Telegram poller started (allowed users: %s)", ", ".join(sorted(allowed)))

    async with httpx.AsyncClient(timeout=35.0) as client:
        while True:
            try:
                resp = await client.get(f"{api}/getUpdates", params={"offset": offset, "timeout": 30})
                resp.raise_for_status()
                updates = resp.json().get("result", [])
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("getUpdates failed, retrying in 5s")
                await asyncio.sleep(5)
                continue

            for update in updates:
                offset = update["update_id"] + 1
                message = update.get("message")
                if not message or "text" not in message:
                    continue

                chat_id = message["chat"]["id"]
                sender_id = str(message["from"]["id"])
                text = message["text"]

                if sender_id not in allowed:
                    logger.warning("refused message from non-allow-listed user %s", sender_id)
                    await _send_message(client, api, chat_id, "Not authorized.")
                    continue

                try:
                    reply = await call_agent(str(chat_id), text)
                except Exception:
                    logger.exception("call_agent failed")
                    reply = "Something went wrong on my end — try again in a moment."

                await _send_message(client, api, chat_id, reply)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_telegram_poller())
