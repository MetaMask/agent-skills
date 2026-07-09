# View / cancel Predict orders and positions

Use when the user wants to review open Predict orders or positions, or cancel orders. Placing
a new order: workflows/predict-place-order.md. Redeeming winnings:
workflows/predict-portfolio.md. Command details: references/predict-trade.md.

## Preconditions

1. `mm predict status` shows `account.setupComplete: true`. If not: workflows/predict-setup.md.
2. For cancelling: you know the scope (one order, one market, one outcome token, or ALL). If
   ambiguous, ask — do not default to `--all`.

## Steps

### 1. Review open orders

```bash
mm predict orders --toon
```

Filter to one market with `--market <condition-id>`; page with `--cursor <cursor>`.
Expected output: open orders with `orderId`, token, side, size, price.
Capture: `orderId` → `<order-id>` for step 3.

### 2. Review positions (if the user asked)

```bash
mm predict positions --toon
```

Expected output: positions with market question, outcome, size, and estimated value. If the
user only wanted a review, report and stop here.

### 3. Confirm the cancel scope with the user

Choose EXACTLY ONE targeting flag and show the user exactly what it matches from step 1:

- One named order → `--order-id <order-id>`.
- All orders in one market → `--market <condition-id>` (list the matching orders).
- All orders on one outcome token → `--asset <token-id>` (list the matching orders).
- Everything → `--all` — say explicitly "this cancels ALL open orders" and list them.

Do not continue until the user explicitly approves the exact scope.

### 4. Cancel

```bash
mm predict cancel --order-id 0x1f9090aae28b8a3dceadf281b0f12828e676c326 --toon
```

Substitute the confirmed targeting flag from step 3 (`--all`, `--market <condition-id>`, or
`--asset <token-id>`). Completes inline; no polling ID.
Expected output: list of cancelled order IDs.

### 5. Verify

```bash
mm predict orders --toon
```

Expected output: the cancelled orders are gone (empty list after `--all`). Report the result.

## Decision points

- User rejects at step 3 → stop. Do not cancel.
- User says "cancel my order" but multiple are open → show the step 1 list and ask which.
- Cancelled order was partially filled → the filled part remains as a position (step 2);
  selling it back is a new order via workflows/predict-place-order.md.
- Position won after resolution → workflows/predict-portfolio.md to redeem.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| `ValidationError` (zero or multiple targets) | Pass exactly one of `--order-id`, `--all`, `--market`, `--asset` |
| `NOT_FOUND` / order not in step 5 list already | Order already filled or cancelled; check `mm predict positions --toon` |
| `PREDICT_SETUP_REQUIRED` | workflows/predict-setup.md, then retry |
| `UNKNOWN` (`fetch failed`) | Transient CLOB failure; retry, check `mm predict status` |
