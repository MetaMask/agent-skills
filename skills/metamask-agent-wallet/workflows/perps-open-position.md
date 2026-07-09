# Open a perp position

Use when the user wants to open a new perpetual futures position (long or short).
Closing or changing an existing position: workflows/perps-close-position.md /
workflows/perps-modify-position.md. Command details: references/perps.md.

## Preconditions

1. `mm doctor` reports `authenticated: true` and `initialized: true`. If not: SKILL.md § Preflight.
2. You know: symbol, side (long/short), size (base asset), leverage. If any is missing, ask —
   do not guess. Symbols: `mm perps markets --venue hyperliquid --toon`.
3. Venue margin covers the position: `mm perps balance --venue hyperliquid --toon` —
   `spendableBalance` ≥ quoted notional / leverage. If not, deposit first
   (`mm perps deposit`, references/perps.md) from Arbitrum USDC.

## Steps

### 1. Verify the market and max leverage

```bash
mm perps markets --venue hyperliquid --symbol BTC --toon
```

Expected output: one row with `symbol`, `maxLeverage`, `markPrice`.
Capture: `maxLeverage` → reject the request if the desired leverage exceeds it.

### 2. Quote the order

```bash
mm perps quote --venue hyperliquid --symbol BTC --side long --size 0.001 --leverage 2 --toon
```

For a limit order append `--type limit --limit-px 60000`.
Expected output: `entryPrice`, `notional`, `estimatedFee`, `estimatedLiquidationPrice`, `warnings`.
Capture: those four fields → shown in step 3.

### 3. Confirm with the user

Show: symbol, side, size, leverage, venue, order type (market/limit), limit price if set,
quoted entry price, notional, estimated fee, estimated liquidation price (note it is an
estimate). Do not continue until the user explicitly approves.

### 4. Open the position

```bash
mm perps open --venue hyperliquid --symbol BTC --side long --size 0.001 --leverage 2 --yes --toon
```

If anything is uncertain (first trade, near margin limits), run the identical command with
`--dry-run` instead of `--yes` first, review, then re-run with `--yes`.
Expected output: `ok: true` with the order/fill result.

### 5. Verify

```bash
mm perps positions --venue hyperliquid --toon
```

Expected output: a row for the new position with matching symbol, side, size, leverage.
Report entry price and liquidation price to the user.

## Decision points

- User rejects at step 3 → stop. Do not open.
- Leverage > `maxLeverage` at step 1 → tell the user the market maximum; re-quote only after
  they pick a valid leverage.
- Insufficient `spendableBalance` → offer `mm perps deposit` (references/perps.md), then restart at step 2.
- `--type limit` without a limit price → ask for the price; `--limit-px` is required.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| `ValidationError` (unknown symbol) | `mm perps markets --venue hyperliquid --toon`; confirm the exact symbol with the user |
| Insufficient margin | `mm perps balance --venue hyperliquid --toon`; deposit USDC or reduce size after user approval |
| Position missing at step 5 (limit order) | The order is resting, not filled — show it via `mm perps orders --venue hyperliquid --toon` |
