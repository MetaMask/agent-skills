# Close a perp position

Use when the user wants to close a perpetual position (fully, partially, or all positions).
Cancelling a resting order instead: `mm perps cancel` (references/perps.md).
Command details: references/perps.md.

## Preconditions

1. `mm doctor` reports `authenticated: true` and `initialized: true`. If not: SKILL.md § Preflight.
2. An open position exists: `mm perps positions --venue hyperliquid --toon` returns a
   non-empty list. If empty: tell the user there is nothing to close and stop.

## Steps

### 1. List open positions

```bash
mm perps positions --venue hyperliquid --toon
```

Expected output: one row per position with symbol, side, size, entry price, unrealized PnL.
Capture: `symbol` → `<symbol>` in step 3; size and unrealized PnL → shown in step 2.

### 2. Confirm with the user

Show: symbol (or "ALL open positions" if the user asked to close everything), current size,
close size (full, or the partial `--size`), side, current unrealized PnL (estimated impact of
closing now), venue. Do not continue until the user explicitly approves.

### 3. Close

```bash
mm perps close --venue hyperliquid --symbol BTC --yes --toon
```

Variants (exactly one form):
- Partial close: append `--size 0.0005` to the command above.
- Close everything: `mm perps close --venue hyperliquid --all --yes --toon` (no `--symbol`, no `--size`).

Expected output: `ok: true` with the close/fill result.

### 4. Verify

```bash
mm perps positions --venue hyperliquid --toon
```

Expected output: the position is gone (full close / `--all`) or shows the reduced size
(partial). Report realized outcome to the user.

## Decision points

- User rejects at step 2 → stop. Do not close.
- User wants to close several but not all symbols → run step 3 once per symbol, confirming each.
- Partial `--size` ≥ position size → treat as a full close; omit `--size`.
- Uncertain market conditions → run step 3 with `--dry-run` instead of `--yes` first, review, re-run.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| `ValidationError` (`--symbol` with `--all`, or `--size` with `--all`) | Use exactly one form from step 3 |
| Position not found | Re-run step 1; the symbol may already be closed or misspelled |
| Position still listed after full close | Wait a few seconds and re-run step 4; venue settlement can lag |
