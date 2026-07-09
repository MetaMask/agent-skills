# Predict portfolio and redeem winnings

Use when the user wants a Predict account overview or to claim winnings from resolved
markets. Cancelling open orders: workflows/predict-manage-orders.md. Command details:
references/predict-trade.md.

## Preconditions

1. `mm predict status` shows `account.setupComplete: true`. If not: workflows/predict-setup.md.
2. Redeeming only works after a market has resolved; unresolved positions are sold via
   workflows/predict-place-order.md instead.

## Steps

### 1. View the portfolio

```bash
mm predict portfolio --toon
```

Expected output: pUSD balance, open positions with estimated value, and redeemable winnings.
If the user only wanted an overview, report and stop here.

### 2. List redeemable positions

```bash
mm predict redeem list --toon
```

Expected output: redeemable positions with `conditionId`, market question, and size. If
empty, report that there is nothing to redeem and stop.
Capture: `conditionId` → `<condition-id>` for step 4.

### 3. Confirm the redeem scope with the user

Choose EXACTLY ONE form and show the user exactly what it covers from step 2:

- One market → positional `<condition-id>` (show its question and size).
- Everything → `--all` — say explicitly "this redeems EVERY winning position" and list all
  affected markets with expected pUSD proceeds.

Do not continue until the user explicitly approves the exact scope.

### 4. Redeem

```bash
mm predict redeem 0x5179f59617e32ce893c4ecc0ee1e4916c65f7a85eb3774c87cdc3430cb1d0d73 --wait --toon
```

For everything: `mm predict redeem --all --wait --toon` (no positional).
Expected output: success once the redemption transaction confirms.
Capture: `pollingId` (only if run without `--wait`) → `<polling-id>` for
`mm predict watch --id <polling-id> --wait`.

### 5. Verify

```bash
mm predict balance --sync --toon
```

Expected output: pUSD increased by the redeemed proceeds; `mm predict redeem list --toon` no
longer lists the redeemed market(s). Report the new balance.

## Decision points

- User rejects at step 3 → stop. Do not redeem.
- User expected a win but step 2 is empty → the market may not be resolved yet; check it with
  `mm predict markets get --market <condition-id> --toon` (`closed` field).
- User wants the proceeds in their EOA → after step 5, withdraw via
  workflows/predict-funding.md.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| `ValidationError` (both or neither of positional / `--all`) | Pass exactly one: a `<condition-id>` positional OR `--all` |
| `NOT_FOUND` on condition ID | Re-run step 2 and copy the exact `conditionId` |
| `PREDICT_SETUP_REQUIRED` | workflows/predict-setup.md, then retry |
| Job stalls without `--wait` | `mm predict watch --id <polling-id> --wait` |
