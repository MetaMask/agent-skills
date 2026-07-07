# Verified perps-open workflow

Extends MetaMask's [perps-open-position](https://github.com/metamask/agent-skills) flow
with one reasoning check inserted between **dry-run** and **open**. Everything else is
unchanged — this does not replace any MetaMask step.

## Flow (verify step inserted at 4)

1. Check balance and deposit if needed.  *(unchanged — mm)*
2. Quote the position. `mm perps quote ...`  *(unchanged — mm)*
3. Dry run. `mm perps open ... --dry-run`  *(unchanged — mm)*
4. **Verify the reasoning.** ← THIS SKILL
5. Confirm with the user and open — **only if step 4 returned ALLOW**. `mm perps open ...`

## Step 4 — the verify gate

After the dry-run succeeds and before asking the user to confirm the real open, verify the
thesis (see [verify-trade.md](../references/verify-trade.md)):

```
verdict = thoughtproof.verify({
  mode: "trade_reasoning",
  claim: "open <side> <symbol> <leverage>x, <size>",
  evidence: "<the agent's thesis> + <the live market data it cites>",
})
```

- `ALLOW` → proceed to step 5 (`mm perps open` without `--dry-run`, after explicit user
  confirmation, exactly as the base workflow requires).
- `UNCERTAIN` → present the objections; the agent may re-plan against them and re-verify.
  Do not auto-open.
- `BLOCK` → stop. Show the objections. `mm perps open` is never run.

## Why here and not in `mm`

MetaMask's `guard` trading-mode and Blockaid already run on the transaction at signing time
(policy + malicious-tx). They do not evaluate whether the *thesis* is true — a short on a
hallucinated RSI passes both and is still a bad trade. Putting the reasoning check between
dry-run and open catches that class one layer before it reaches the signer, without touching
MetaMask's pipeline.

## Example (from a real dryrun)

- Clean 2x long, thesis consistent with the market data → `ALLOW` → `mm perps open` ran.
- Short built on an invented RSI + fabricated death-cross + made-up SMA200 → `BLOCK` →
  `mm` never invoked.
