# Verify a trade before opening a position

Use before `mm perps open` when an agent has produced a trade thesis. Checks whether
the reasoning is faithful to the evidence — catches theses built on hallucinated
indicators, invented price levels, or logic that contradicts the actual market data,
all of which pass structural checks and are still wrong.

## When to run

After the agent decides `side / size / leverage` with a thesis, and after `mm perps quote`
+ `mm perps open --dry-run`, but **before** the real `mm perps open`.

## Call

```
verdict = thoughtproof.verify({
  mode: "trade_reasoning",
  claim: "<the decision: open <side> <symbol> <leverage>x>",
  evidence: "<thesis + live market data the thesis cites (RSI, SMA, trend, changes)>",
})
```

Returns `{ verdict: ALLOW | BLOCK | UNCERTAIN, confidence, objections[], reasoning }`.
Each objection is bound to a specific reasoning step (which claim failed and why).

## Gate

| Verdict | Action |
|---|---|
| `ALLOW` | Proceed to `mm perps open` (MetaMask's own guard mode + Blockaid still apply on top). |
| `UNCERTAIN` | Surface the objections to the user; do NOT auto-execute. The agent may re-plan against the specific objections and re-verify. |
| `BLOCK` | Do not open. Show the objections. `mm` is never invoked. |

## Honesty

- The verdict is a real Sentinel `trade_reasoning` call — not hand-set.
- **This verifies reasoning, it does not guarantee safety or outcomes.** A verdict that the
  thesis is faithful to the evidence is not a claim that the trade will be profitable or that
  the transaction is safe — it only says the stated reasoning holds against the stated data.
- This does **not** replace MetaMask's guard mode or Blockaid. It is the reasoning layer
  above them: a thesis can be faithful (this passes) and the transaction still needs
  MetaMask's policy + malicious-tx checks, and vice-versa.
