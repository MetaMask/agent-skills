# Quote and place a prediction order

Use when the user wants to buy or sell shares in a Polymarket outcome. Cancelling or viewing
orders: workflows/predict-manage-orders.md. Command details: references/predict-trade.md.

## Preconditions

1. `mm predict status` shows `account.setupComplete: true`. If not: workflows/predict-setup.md.
2. pUSD balance covers the order (size × price for buys): `mm predict balance --sync --toon`.
   If insufficient: workflows/predict-funding.md.
3. You know: market, outcome, side (buy/sell), size (shares), and price or "market". If any
   is missing, ask — do not guess.

## Steps

### 1. Get the outcome token ID

```bash
mm predict markets get --market bitcoin-above-52k-on-july-9-2026 --toon
```

Find the market first if needed: workflows/predict-markets.md.
Expected output: market detail with per-outcome token IDs, tick size, and minimum order size.
Map the user's intended outcome to its token ID — token IDs are not market IDs.
Capture: outcome token ID → `<token-id>` for steps 2 and 4.

### 2. Quote the order

```bash
mm predict quote --token-id 21742633143463906290569050155826241533067272736897614950488156847949938836455 --side buy --size 10 --limit-price 0.55 --toon
```

Expected output: estimated cost, average fill price, and fillable size.

### 3. Confirm with the user

Show ALL of: market question, outcome, token ID, side, size (shares), price per share, order
type (`GTC` default; `GTD` needs `--expiration <unix>`; `FOK`/`FAK` are market-style), total
cost for buys, and the quote from step 2. Warn if the price is 1 or the market's end date has
passed but UMA resolution is pending — prices then do not reflect true odds. Do not continue
until the user explicitly approves.

### 4. Place the order

```bash
mm predict place --token-id 21742633143463906290569050155826241533067272736897614950488156847949938836455 --side buy --size 10 --price 0.55 --order-type GTC --toon
```

Orders are signed by the Predict deposit wallet, not the owner EOA.
Expected output: order record with `orderId` and status, or a job ID.
Capture: `orderId` → `<order-id>` for cancel; a job ID → `<polling-id>` for
`mm predict watch --id <polling-id> --wait`.

### 5. Verify

```bash
mm predict orders --toon
```

Expected output: the new order listed as open (limit orders), or absent because it filled
(FOK/FAK / crossing limit). Check fills with `mm predict positions --toon` and report.

## Decision points

- User rejects at step 3 → stop. Do not place.
- Quote shows insufficient fillable size or a bad price → show the book
  (`mm predict book --token-id <token-id> --toon`) and re-confirm a new price at step 3.
- GTD order → add `--expiration <unix>` (`date +%s` plus the desired lifetime); `--post-only`
  is invalid with FOK/FAK.
- Job ID returned at step 4 → `mm predict watch --id <polling-id> --wait --toon` before step 5.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| `PREDICT_SETUP_REQUIRED` | workflows/predict-setup.md, then retry |
| `WALLET_ERROR` (insufficient pUSD) | `mm predict balance --sync`; deposit via workflows/predict-funding.md |
| `ValidationError` | Price outside (0, 1], size below market minimum, `--post-only` with FOK/FAK, or `--expiration` without GTD; fix and retry |
| `NOT_FOUND` on token ID | Re-run step 1 and copy the exact token ID |
