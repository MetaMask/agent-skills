# Perps Modify Position Workflow

Use this workflow when the user wants to modify leverage, take-profit, or stop-loss on an existing position.

Reference command syntax in `references/perps.md`.

## Flow

1. Check open positions.
2. Dry run the modification.
3. Confirm with the user and modify.

## Check Positions

```bash
mm-dev perps positions --venue hyperliquid
```

## Dry Run

Preview the modification before executing:

```bash
mm-dev perps modify --venue hyperliquid --symbol BTC --leverage 10 --dry-run
mm-dev perps modify --venue hyperliquid --symbol ETH --tp 3000 --sl 2000 --dry-run
```

At least one of `--leverage`, `--tp`, or `--sl` must be provided.

## Modify

Remove `--dry-run` only after explicit user confirmation:

```bash
mm-dev perps modify --venue hyperliquid --symbol BTC --leverage 10
mm-dev perps modify --venue hyperliquid --symbol ETH --tp 3000 --sl 2000
```

Do not add `--yes` unless the user explicitly asked for unattended execution.
