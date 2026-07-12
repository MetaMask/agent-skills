# Telegram bridge workflow

Use this workflow when wiring an existing `mm`-backed agent up to Telegram.
Assumes the agent already runs continuously somewhere (a server, a
long-running process) — this bridge is a background task added to that
same process, not a new service.

## Flow

1. Register a bot with `@BotFather` on Telegram; get the bot token.
2. Get the numeric Telegram user ID(s) that should be allowed to use the bot
   (message `@userinfobot` to find your own).
3. Add a long-polling background task to the agent's process (see
   `scripts/telegram_poller.py`) that:
   - Polls Telegram's `getUpdates` endpoint in a loop.
   - Checks the sender's user ID against the allow-list. Refuses (and does
     NOT call the agent) if the sender isn't on it.
   - Calls the agent runner directly — in-process, not over HTTP to a
     separate service — with the message text.
   - Sends the reply back via `sendMessage`.
4. Start the poller as a background task alongside the agent's normal
   startup (a `lifespan`/startup hook, a supervised subprocess, whatever
   your runtime already uses for background work).
5. Set the bot token and allow-list as environment variables / secrets on
   wherever the agent already runs. No new hosting target.

Don't skip step 2's fail-closed check — see "Edge cases" below.

## Per-chat conversation continuity

Key your agent's conversation/thread state by the Telegram chat ID, the same
way you'd key it by a session ID for any other transport. Each distinct
Telegram chat gets its own stable thread, so follow-up messages ("what did I
just ask?", a multi-turn preview→confirm→execute flow) have the context they
need.

## The gate-bypass decision

If the agent has an action-authority gate — some check that runs before a
fund-moving or otherwise consequential action executes — decide explicitly
whether Telegram-triggered calls go through it. The pattern that keeps this
decision visible in the code (not just in a commit message):

```python
# gate.py
from contextvars import ContextVar

telegram_mode: ContextVar[bool] = ContextVar("telegram_mode", default=False)

async def gate_or_refusal() -> str | None:
    if telegram_mode.get():
        return None  # deliberately bypassed for Telegram — see SKILL.md
    # ... the real gate check ...
```

```python
# telegram_poller.py, around the call into the agent
token = telegram_mode.set(True)
try:
    result = await run_agent(...)
finally:
    telegram_mode.reset(token)
```

A `ContextVar` (not a module-level bool) keeps this isolated per
asyncio task — it can't leak into a concurrent request on the agent's
primary interface. Whichever way you decide, the flag makes the decision a
single, greppable line instead of a scattered assumption.

## Edge cases

- **Allow-list not configured**: refuse to start the poller entirely, and
  log why. Never fall back to "allow everyone" — that's the single access
  control this whole bridge has.
- **Message from a non-allow-listed user**: reply with a plain refusal (or
  silently ignore, if you'd rather not confirm the bot exists to strangers)
  and do not call the agent runner at all — the refusal must happen before
  the agent sees the message, not after.
- **Long replies**: Telegram caps messages at 4096 characters; chunk longer
  replies rather than silently truncating a wallet-relevant answer.
- **`getUpdates` failures** (network blip, Telegram-side issue): catch,
  log, back off briefly, and keep polling — don't let a transient failure
  kill the background task permanently.
- **Silent logging**: if you're not seeing expected log lines in production,
  confirm your logging is actually configured with a level/handler — a
  default Python logger config drops `INFO` (and even some `WARNING`)
  messages with no error, which looks identical to "the code path never
  ran."
