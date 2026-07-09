# Predict deposit / withdraw pUSD

Use when the user wants to fund the Predict deposit wallet or take funds out. Trading:
workflows/predict-place-order.md. Command details: references/predict-account.md.

Chooser: if money moves INTO the deposit wallet → Deposit path (steps 2a-4a). If money moves
OUT to an EOA → Withdraw path (steps 2b-4b).

## Preconditions

1. `mm predict status` shows `account.setupComplete: true`. If not: workflows/predict-setup.md.
2. You know the amount. If not stated, ask — do not guess.
3. Deposit only: owner EOA holds enough USDC.e plus POL for gas on Polygon:
   `mm wallet balance --chain 137`.

## Steps

### 1. Check the deposit-wallet balance

```bash
mm predict balance --sync --toon
```

Expected output: current pUSD balance, approvals, and setup status.

### 2a. Deposit — confirm with the user

Show: amount, source (owner EOA USDC.e on Polygon, chain 137), destination (Predict deposit
wallet, credited as pUSD — the CLI converts USDC.e to pUSD). Do not continue until the user
explicitly approves.

### 3a. Deposit

```bash
mm predict deposit --amount 5 --wait --toon
```

Amount is human-readable USDC.e (`5`, `100`), not atomic units.
Expected output: success once the deposit job completes.
Capture: `pollingId` (only if run without `--wait`) → `<polling-id>` for
`mm predict watch --id <polling-id> --wait`.

### 4a. Verify the deposit

```bash
mm predict balance --sync --toon
```

Expected output: pUSD increased by the deposited amount. Report the new balance.

### 2b. Withdraw — confirm with the user

Show: amount and recipient. When `--to` is omitted, say "owner EOA" explicitly. Do not
continue until the user explicitly approves.

### 3b. Withdraw

```bash
mm predict withdraw --amount 10 --wait --toon
```

Different recipient: add `--to 0x742d35Cc6634C0532925a3b844Bc454e4438f44e`. The CLI validates
the amount against the on-chain deposit-wallet balance before signing.
Expected output: success once the withdraw job completes.
Capture: `pollingId` (only if run without `--wait`) → `<polling-id>` for
`mm predict watch --id <polling-id> --wait`.

### 4b. Verify the withdrawal

```bash
mm wallet balance --chain 137 --toon
```

Expected output: recipient balance increased; `mm predict balance --sync` shows the reduced
pUSD balance.

## Decision points

- User rejects at the confirmation step → stop. Do not execute.
- Owner EOA has POL but no USDC.e on Polygon → swap to USDC.e first (workflows/swap.md), or
  bridge from another chain (workflows/bridge.md), then return to step 2a.
- Withdraw amount exceeds the pUSD balance → report the balance from step 1 and ask for a
  smaller amount.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| `WALLET_ERROR` (deposit) | Insufficient USDC.e or POL gas: `mm wallet balance --chain 137`; fund or reduce amount |
| `WALLET_ERROR` (withdraw) | Insufficient pUSD: `mm predict balance --sync`; reduce amount |
| `PREDICT_SETUP_REQUIRED` | Run workflows/predict-setup.md, then retry |
| Job stalls without `--wait` | `mm predict watch --id <polling-id> --wait` |
