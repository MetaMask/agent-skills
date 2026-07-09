# Predict first-time setup

Use when Predict has never been set up for this wallet, or `setupComplete: false` blocks a
trading/funding command. Repairing stale credentials/approvals only: jump to Decision points.
Command details: references/predict-account.md.

## Preconditions

1. `mm doctor` reports `authenticated: true` and `initialized: true`. If not: SKILL.md § Preflight.
2. The owner EOA holds POL on Polygon for gas: `mm wallet balance --chain 137`. If empty,
   fund the wallet first (references/wallet.md).
3. You know whether the user wants real trading (`mainnet`) or paper trading (`testnet`).
   If not stated, ask — do not guess.

## Steps

### 1. Check geoblock

```bash
mm predict geoblock --toon
```

Expected output: `data.result.blocked: false`. If `blocked: true`, stop — Predict is
unavailable from this region; do not attempt setup.

### 2. Set the trading mode

```bash
mm predict mode mainnet --toon
```

Positional-only; replace `mainnet` with `testnet` for paper trading.
Expected output: `data.result.mode` matching the requested mode.

### 3. Confirm with the user

Show: that setup deploys a Predict deposit wallet, creates trading credentials, and grants
token approvals on Polygon (chain 137), plus the chosen mode. Do not continue until the user
explicitly approves.

### 4. Run one-time setup

```bash
mm predict setup --wait --toon
```

Expected output: success after credential, deposit-wallet, and approval jobs complete.
Capture: `pollingId` (only if run without `--wait`) → `<polling-id>` for
`mm predict watch --id <polling-id> --wait`.

### 5. Verify

```bash
mm predict status --toon
```

Expected output: `account.setupComplete: true`, `account.deployed: true`,
`account.credentials: true`.
Capture: `account.depositWalletAddress` → report to the user for funding
(workflows/predict-funding.md).

## Decision points

- Step 1 fails `UNKNOWN` (`fetch failed`) repeatedly → tell the user the geoblock probe is
  unreachable and continue; `mm predict setup` itself aborts `PREDICT_GEOBLOCKED` if restricted.
- Step 5 shows `credentials: false` → run `mm predict auth --refresh --toon`, then re-verify.
- Step 5 shows `deployed: true` but `setupComplete: false` (approvals missing) → confirm with
  the user, run `mm predict approve --wait --toon`, then re-verify with `mm predict status`.
- User rejects at step 3 → stop. Nothing has changed on-chain.
- Setup succeeded and the user wants to trade → workflows/predict-funding.md, then
  workflows/predict-place-order.md.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| `PREDICT_GEOBLOCKED` | Region restricted; stop. Re-check with `mm predict geoblock` |
| `WALLET_ERROR` / gas failure | Owner EOA lacks POL on Polygon: `mm wallet balance --chain 137`, fund, retry step 4 |
| `UNKNOWN` (`fetch failed`) | Transient back-end failure; retry, check `mm predict status` |
| Setup stalls without `--wait` | `mm predict watch --id <polling-id> --wait`, then `mm predict status` |
