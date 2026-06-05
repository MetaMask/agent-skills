# Predict Trading Workflow

Use this workflow when the user wants to set up prediction market trading, fund the deposit wallet, quote/place orders, or manage Predict orders and positions.

Reference command syntax in `../references/predict.md`. Cross-chain funding: [bridge.md](bridge.md) (§ Fund prediction markets on Polygon).

## End-to-end flow

Typical order:

1. One-time setup (if needed) — `predict setup`, credentials, approvals.
2. Fund — ensure pUSD or USDC.e on Polygon; bridge from other chains when needed.
3. Resolve market and outcome token ID.
4. Quote and place.
5. Manage orders/positions; close or cancel when the user asks to exit.

Complete **funding before** heavy market search when the user already gave you an amount to trade.

## Mandatory: Polygon USDC.e before `predict deposit`

```bash
mm-dev wallet balance --chain 137 --token 0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174 --json
mm-dev wallet balance --chain 137 --token 0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359 --json
```

| Token | Polygon contract | Used by `predict deposit`? |
| --- | --- | --- |
| **USDC.e** (bridged) | `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174` | **Yes** — wrap source for pUSD |
| Native USDC (Circle) | `0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359` | **No** — balance here does not fund deposit |

Required: USDC.e ≥ `--amount` (pUSD) + ~$1 POL on Polygon for gas.

If USDC.e is too low: do **not** retry `predict deposit` in a loop — `execution reverted` usually means native USDC only or insufficient USDC.e.

## Fund from another chain

Polymarket predict uses Polygon (`137`). If USDC.e on the owner EOA is insufficient but USDC exists elsewhere, bridge before `predict deposit` (see [swap.md](swap.md), [bridge.md](../workflows/bridge.md)):

```bash
mm-dev wallet balance --chain 8453 --token USDC
mm-dev swap quote --from USDC --to USDC --amount <amount> --from-chain 8453 --to-chain 137
mm-dev swap execute --quote-id <quote-id>
mm-dev wallet balance --chain 137 --token 0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174
mm-dev predict deposit --amount <pUSD> --wait
```

Use the chain ID where the wallet actually holds USDC (`8453` Base, `42161` Arbitrum, `1` Ethereum). Include slippage buffer in the bridge amount. Re-check USDC.e (`0x2791…`), not native USDC (`0x3c499…`), before depositing.

## One-Time Setup

Choose the Predict mode, run setup, and check backend status:

```bash
mm-dev predict mode mainnet
mm-dev predict setup --wait
mm-dev predict status
```

`predict setup --wait` blocks until credential, deposit-wallet, and approval jobs complete. Without `--wait`, watch returned jobs with `mm-dev predict watch`.

If setup or approvals look stale later:

```bash
mm-dev predict auth --refresh
mm-dev predict approve --wait
mm-dev predict balance --sync
```

`predict setup` and `predict deposit` use `--wait`; do not add `--yes` to those commands.

## Fund the Deposit Wallet

Check deposit wallet status:

```bash
mm-dev predict balance --sync
```

Fund pUSD:

```bash
mm-dev predict deposit --amount 100 --wait --json
```

`--amount` is in pUSD. The owner EOA needs enough Polygon USDC and POL for gas to complete the deposit transaction.

## Withdraw from the Deposit Wallet

Check balance first:

```bash
mm-dev predict balance --sync
```

Withdraw pUSD to the owner EOA (default) or a specified address:

```bash
mm-dev predict withdraw --amount 50 --wait
mm-dev predict withdraw --amount 10 --to 0xRecipient... --wait
```

The CLI validates the amount against the on-chain deposit wallet balance before signing. Confirm amount and recipient with the user before executing.

## Find the Right Market

Search can return loosely related markets, so inspect the selected market before quoting:

```bash
mm-dev predict markets search "Knicks NBA Finals" --limit 5 --json
mm-dev predict markets get will-the-new-york-knicks-win-the-2026-nba-finals --json
```

The market detail prints outcome token IDs. Outcome token IDs are not market IDs; use the token ID for `quote`, `place`, `book`, and `balance --token-id`.

If search is noisy, list active markets and filter manually:

```bash
mm-dev predict markets list --active --limit 50 --json
```

## Quote, Then Place

Preview the order cost and fill before placing:

```bash
mm-dev predict quote \
  --token-id <outcomeTokenId> \
  --side buy --size 100 --limit-price 0.55
```

After the user confirms token ID, outcome, side, size, price, and order type:

```bash
mm-dev predict place \
  --token-id <outcomeTokenId> \
  --side buy --size 100 --price 0.55 \
  --order-type GTC
```

`--order-type` is one of `GTC`, `GTD`, `FOK`, or `FAK`. `--post-only` only applies to GTC/GTD. `--expiration` is unix seconds for GTD.

## Manage Orders and Positions

```bash
mm-dev predict orders
mm-dev predict orders --market <condition-id>
mm-dev predict positions
mm-dev predict positions --market <condition-id>
mm-dev predict cancel --order-id <order-id>
mm-dev predict cancel --market <condition-id>
mm-dev predict cancel --asset <outcomeTokenId>
mm-dev predict cancel --all
```

`predict cancel --all` cancels every open order. Require explicit confirmation.

## Watch Async Jobs

```bash
mm-dev predict watch --id <job-id> --wait
```

Use this for setup, approve, deposit, withdraw, and order jobs that have not reached a terminal state.

## Safety Notes

- Prices are 0-1 floats. Treat `--price 1` as suspicious unless the user explicitly confirms.
- Trades are signed by the deposit wallet address shown by `mm-dev predict balance`, not necessarily the connected owner EOA.
- Always inspect the market to map the user's intended outcome to the correct token ID.
