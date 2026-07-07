---
name: metamask-agent-verified-trading
description: Use before an AI agent opens a perps trade via mm — verifies whether the trade's REASONING holds (is the thesis faithful to the live market data, or built on a hallucinated indicator / invented price level / logic that contradicts the data?). This is the failure class a policy rule or a malicious-tx scanner cannot catch: a structurally valid, policy-compliant trade that is still wrong because its premise is false. Runs one layer above mm, additive, no changes to MetaMask's signing pipeline. (Also carries an optional authorization check for raw wallet actions — see the note at the end.)
license: MIT
metadata:
  author: thoughtproof
  version: "0.1.0"
  cliVersion: "4.0.0"
  upstream: https://github.com/ThoughtProof/verified-wallet-agent
---

# ThoughtProof Verified Trading Skill (pre-trade reasoning guard)

A **third-party safety skill** an agent installs alongside the MetaMask wallet skills and
runs **before** it opens a trade via `mm`. It wraps ThoughtProof's `trade_reasoning`
verdict and turns a proposed trade into an `mm perps open` command — **only on an explicit
ALLOW**. On anything else, `mm` is never invoked.

## The one axis this checks (and why nothing else does)

MetaMask already guards two axes, both **deterministic / rule-based**:

| Layer | Question | Mechanism | Could be a rule? |
|---|---|---|---|
| `mm wallet trading-mode guard` + `wallet policy` | "Within policy?" | outflow caps, whitelists | yes (it is one) |
| Blockaid | "Is this transaction malicious?" | known-scam / drainer scan | yes (pattern match) |
| **This skill** | **"Is the reasoning behind this trade true?"** | adversarial reasoning verdict | **no — this is the point** |

A trade can be within policy, non-malicious, and structurally perfect — and still be built
on a **hallucinated RSI, an invented price level, or a thesis that contradicts the actual
market data**. No policy rule and no transaction scanner catches that, because the transaction
is fine; the *decision* is wrong. That is the single axis this skill verifies, and it is
**not** reducible to a deterministic rule — it needs the reasoning check. It is **additive**:
no hook into MetaMask's (non-bypassable, by design) signing pipeline, **zero changes to
MetaMask**. The guard lives in the agent, one layer above `mm`.

## Flow

```
trade  = agent.plan()                    # side / size / leverage + thesis
verdict = thoughtproof.verify(trade)     # trade_reasoning  ← THIS SKILL
if verdict == ALLOW:  mm perps open ...  # MetaMask's guard mode + Blockaid still apply on top
else:                 mm is NEVER invoked. The trade never reaches the signer.
```

Fail-closed: only an explicit ALLOW proceeds. UNCERTAIN and BLOCK stop before `mm`.

## Routing

| Intent | Reference |
|---|---|
| Verify a proposed trade before opening a perps position | [verify-trade.md](references/verify-trade.md) |
| The verified perps-open workflow (verify between dry-run and open) | [workflows/verified-perps-open.md](workflows/verified-perps-open.md) |
| *(Optional)* authorization check for raw wallet actions | [verify-wallet-action.md](references/verify-wallet-action.md) |

## Verification status (verified 2026-07-06, not claimed)

In a dryrun: a clean 2x long whose thesis matched the market data was `ALLOW`ed and executed;
a short built on an **invented RSI, a fabricated death-cross, and a made-up SMA200** was
`BLOCK`ed one layer before the order reached `mm`. That is the axis this skill verifies.
Command mappings verified against `@metamask/agentic-cli` v4.0.0 (`mm transfer`, `mm swap
execute`, `mm wallet send-transaction`, `mm wallet sign-typed-data` — flags checked via
`mm <cmd> --help`, 2026-07-07).

## Optional: authorization check for raw wallet actions

The same guard shape also exists for raw wallet actions (approve / transfer / permit /
bridge / swap) via Sentinel's `action_authorization` mode — it checks scope containment,
recipient integrity, and least-privilege. This overlaps more with what `wallet policy` and
`guard mode` already do deterministically, so it is **secondary** — included only because it
was built and dryrun-verified (0 false ALLOWs across 10 drain vectors, v4.0.0). See
[verify-wallet-action.md](references/verify-wallet-action.md) if useful. The **reasoning
check above is the part that isn't reducible to a rule** — that's the reason this skill exists.

---

_ThoughtProof — verify the decision, not just the transaction._
