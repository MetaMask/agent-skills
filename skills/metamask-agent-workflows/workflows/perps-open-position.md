# Perps Open Position Workflow

Use this workflow when the user wants to open a new perpetual position.

Reference command syntax in `references/perps.md`.

## Flow

1. Check balance and deposit if needed.
2. Quote the position.
3. Dry run.
4. Confirm with the user and open.

## Check Balance

```bash
mm-dev perps balance --venue hyperliquid
```

If available margin is zero or insufficient, deposit USDC before proceeding:

```bash
mm-dev perps deposit --venue hyperliquid --amount <amount> --asset USDC
```

The default `--source-chain` is Arbitrum mainnet (`eip155:42161`). Do not assume other chains are supported unless the CLI confirms it.

To confirm a deposit, wait briefly and poll `mm-dev perps balance`.

## Quote

Always quote before opening:

```bash
mm-dev perps quote --venue hyperliquid --symbol BTC --side long --size 0.01 --leverage 5
```

Show the user estimated entry, notional, fees, liquidation price, side, size, leverage, and venue before proceeding.

## Dry Run

Preview the order before signing:

```bash
mm-dev perps open --venue hyperliquid --symbol BTC --side long --size 0.01 --leverage 5 --dry-run
```

For limit orders, include `--type limit --limit-px <price>`.

`--max-slippage-bps` is the slippage cap in basis points for IOC market pricing.

## Open

Remove `--dry-run` only after explicit user confirmation:

```bash
mm-dev perps open --venue hyperliquid --symbol BTC --side long --size 0.01 --leverage 5
```

Do not add `--yes` unless the user explicitly asked for unattended execution.
