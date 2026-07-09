# Modify a perp position

Use when the user wants to change leverage, take-profit (TP), or stop-loss (SL) on an
existing perpetual position. Changing size: close partially (workflows/perps-close-position.md)
or open more (workflows/perps-open-position.md). Command details: references/perps.md.

## Preconditions

1. `mm doctor` reports `authenticated: true` and `initialized: true`. If not: SKILL.md § Preflight.
2. An open position exists for the symbol: `mm perps positions --venue hyperliquid --toon`.
3. At least one change is specified: new leverage, TP price, or SL price. If none, ask —
   `mm perps modify` requires at least one of `--leverage`, `--tp`, `--sl`.

## Steps

### 1. Read the current position

```bash
mm perps positions --venue hyperliquid --toon
```

Expected output: a row for the symbol with current side, size, leverage, liquidation price.
Capture: `symbol` → `<symbol>` in step 3; current leverage/TP/SL → the "old" values in step 2.

### 2. Confirm with the user

Show: symbol, venue, and each changed field as old → new (leverage, TP price, SL price).
Sanity-check against the position's side: for a long, TP above and SL below the current mark
price; inverted for a short — warn if not. Warn that raising leverage moves the liquidation
price closer. Do not continue until the user explicitly approves.

### 3. Modify

```bash
mm perps modify --venue hyperliquid --symbol BTC --leverage 10 --yes --toon
```

Include only the flags being changed, e.g. TP/SL only:
`mm perps modify --venue hyperliquid --symbol ETH --tp 3000 --sl 2000 --yes --toon`.
Expected output: `ok: true` with the updated values.

### 4. Verify

```bash
mm perps positions --venue hyperliquid --toon
```

Expected output: the position row reflects the new leverage and/or trigger prices. Report the
new liquidation price to the user if leverage changed.

## Decision points

- User rejects at step 2 → stop. Do not modify.
- New leverage exceeds the market's max → check `maxLeverage` via
  `mm perps markets --venue hyperliquid --symbol BTC --toon`; ask for a valid value.
- TP/SL on the wrong side of the mark price → warn and re-confirm before running.
- Uncertain → run step 3 with `--dry-run` instead of `--yes` first, review, re-run.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| `ValidationError` (none of `--leverage`/`--tp`/`--sl` given) | Ask the user which field to change; pass at least one |
| Position not found | Re-run step 1; confirm the exact symbol |
| Leverage above market max | Read `maxLeverage` from `mm perps markets --symbol <symbol>`; re-confirm a valid value |
