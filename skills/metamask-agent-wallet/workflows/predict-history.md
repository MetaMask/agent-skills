# Predict history workflow

Use this workflow to review past Predict trades and redemptions.

Reference command syntax in `references/predict.md`.

## List recent trades

```bash
mm predict history --toon
```

Each trade row includes a settlement `result` (`won`, `lost`, or `pending`) and, if redeemed, the `amountWon` payout. Use `--side buy` or `--side sell` to filter by direction.

## List redemptions

```bash
mm predict history --type redeem --toon
```

## Inspect a specific market

Drill into history for a single condition:

```bash
mm predict history get <CONDITION_ID> --toon
mm predict history get <CONDITION_ID> --type redeem --toon
```

## Paginate results

When `hasMore` is `true`, use the next-page hint from the CLI output:

```bash
mm predict history --limit 50 --offset 50 --toon
```

## Filter by time range

Use unix timestamps to scope the window:

```bash
mm predict history --start 1719792000 --end 1719878400 --toon
```

## Sort results

```bash
mm predict history --sort-by cash --sort-direction desc --toon
```

Available sort fields: `timestamp` (default), `tokens`, `cash`.
