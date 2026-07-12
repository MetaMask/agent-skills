---
name: metamask-agent-telegram-bridge
description: Use when the user wants to expose an mm-backed agent over Telegram (or a similar chat-bot messaging API) — "add a Telegram bot", "bridge my agent to Telegram", "let me talk to my wallet agent from my phone". Covers the in-process long-polling pattern, the fail-closed allow-list, and the access-control decision this introduces.
license: MIT
metadata:
  author: metamask
  version: "1.0.0"
  cliVersion: "4.0.0"
---

# MetaMask Agent Telegram Bridge

Exposes an `mm`-backed agent (whatever already drives your wallet actions —
an OpenAI Agents SDK agent, or equivalent) over Telegram, so a user can send
it messages from their phone and get real tool-backed replies back.

Reference implementation and the full flow: `workflows/telegram-bridge.md`.
A runnable skeleton is at `scripts/telegram_poller.py`.

## Before you build this, read the callout below

The natural instinct is to route the bridge through whatever agent framework
is already hosting the bot, and prompt-engineer its own reasoning loop into a
"pure relay" that forwards every message verbatim. **That doesn't hold up.**
If forwarding depends on a model choosing to follow an instruction rather than
a guaranteed code path, there is no hard guarantee every message actually gets
forwarded rather than improvised — an unusual message can get an
LLM-invented reply instead of a real tool-backed one. This skill uses a
deterministic alternative instead: a plain long-polling loop that calls the
agent runner directly, in-process, no LLM reasoning in between the inbound
message and the decision to forward it.

## Access control is the whole security model — decide it deliberately

A Telegram bridge is very often reachable with a WEAKER trust boundary than
whatever primary interface (a web UI, a CLI) the agent already has — because
the bridge is a new, separate entry point, it's easy to wire it up without
thinking about who else can reach it. Two things this skill insists on:

1. **A fail-closed allow-list of Telegram user IDs.** If the allow-list isn't
   configured, the bridge should refuse to start — never default to
   open-to-anyone.
2. **If your agent has its own action-authority gate** (an on-chain check, a
   policy engine, a human-approval step — anything that decides whether a
   given action is currently authorized before it executes), **decide
   explicitly whether Telegram-triggered actions go through that gate or
   bypass it, and document the decision inline in the code, not just in a
   PR description.** Bypassing it can be the right call — Telegram's own
   allow-list may already be a sufficient trust boundary for your use case —
   but it must be a decision someone made on purpose, not an accidental gap
   discovered later. See "The gate-bypass decision" in
   `workflows/telegram-bridge.md` for the concrete pattern (a context-scoped
   flag the gate check inspects, set only for the duration of a
   Telegram-triggered call).

## Stack

Nothing exotic: `mm`, an agent runner capable of being called as a plain
function/method (not required to be any specific SDK), any async runtime
that can host a persistent background task alongside whatever's already
serving the agent, and an HTTP client that can hit Telegram's Bot API
directly (`getUpdates` / `sendMessage`) — no Telegram SDK needed. Runs
alongside the agent's existing process; no new service or container
required.
