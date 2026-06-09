# Predict Trading Workflow

Use this workflow when the user wants to set up prediction market trading, fund the deposit wallet, quote/place orders, or manage Predict orders and positions.

Reference command syntax in `../references/predict.md`.

## One-Time Setup

Choose the Predict mode, run setup, and check backend status:

```bash
mm predict mode mainnet
mm predict setup --wait
mm predict status
```

`predict setup --wait` blocks until credential, deposit-wallet, and approval jobs complete. Without `--wait`, watch returned jobs with `mm predict watch`.

Polymarket is geoblocked in some regions. `mm predict setup` checks the caller's IP first and aborts with `PREDICT_GEOBLOCKED` before any wallet interaction if the region is restricted. To check region status independently, run:

```bash
mm predict geoblock
```

If setup or approvals look stale later:

```bash
mm predict auth --refresh
mm predict approve --wait
mm predict balance --sync
```

`predict setup` and `predict deposit` use `--wait`; do not add `--yes` to those commands.

## Fund the Deposit Wallet

Check deposit wallet status:

```bash
mm predict balance --sync
```

Fund pUSD:

```bash
mm predict deposit --amount 100 --wait --json
```

`--amount` is in pUSD. The owner EOA needs enough Polygon USDC and POL for gas to complete the deposit transaction.

## Withdraw from the Deposit Wallet

Check balance first:

```bash
mm predict balance --sync
```

Withdraw pUSD to the owner EOA (default) or a specified address:

```bash
mm predict withdraw --amount 50 --wait
mm predict withdraw --amount 10 --to 0xRecipient... --wait
```

The CLI validates the amount against the on-chain deposit wallet balance before signing. Confirm amount and recipient with the user before executing.

## Find the Right Market

Search can return loosely related markets, so inspect the selected market before quoting:

```bash
mm predict markets search "Knicks NBA Finals" --limit 5 --json
mm predict markets get will-the-new-york-knicks-win-the-2026-nba-finals --json
```

The market detail prints outcome token IDs. Outcome token IDs are not market IDs; use the token ID for `quote`, `place`, `book`, and `balance --token-id`.

If search is noisy, list active markets and filter manually:

```bash
mm predict markets list --active --limit 50 --json
```

To browse by topic, use events, series, and tags. Resolve a tag slug or ID first, then filter:

```bash
mm predict tags list --limit 50 --json
mm predict events list --tag-slug sports --active --limit 10 --json
mm predict events get <event-slug-or-id> --json
mm predict series list --recurrence weekly --limit 10 --json
```

These browse-only commands do not return outcome token IDs. Drill into a specific market with `mm predict markets get <slug>` before quoting or placing.

## Quote, Then Place

Preview the order cost and fill before placing:

```bash
mm predict quote \
  --token-id <outcomeTokenId> \
  --side buy --size 100 --limit-price 0.55
```

After the user confirms token ID, outcome, side, size, price, and order type:

```bash
mm predict place \
  --token-id <outcomeTokenId> \
  --side buy --size 100 --price 0.55 \
  --order-type GTC
```

`--order-type` is one of `GTC`, `GTD`, `FOK`, or `FAK`. `--post-only` only applies to GTC/GTD. `--expiration` is unix seconds for GTD.

## Manage Orders and Positions

```bash
mm predict orders
mm predict orders --market <condition-id>
mm predict positions
mm predict positions --market <condition-id>
mm predict cancel --order-id <order-id>
mm predict cancel --market <condition-id>
mm predict cancel --asset <outcomeTokenId>
mm predict cancel --all
```

`predict cancel --all` cancels every open order. Require explicit confirmation.

## Portfolio and Redeeming Winnings

Get a single snapshot of balance, open positions, and redeemable winnings:

```bash
mm predict portfolio --json
```

After a market resolves, list and claim winning positions:

```bash
mm predict redeem list --json
mm predict redeem <condition-id> --wait
mm predict redeem --all --wait
```

`predict redeem --all` redeems every winning position. Confirm the target (condition ID or `--all`) with the user before executing. With `--wait`, the CLI polls for the redemption transaction receipt.

## Watch Async Jobs

```bash
mm predict watch --id <job-id> --wait
```

Use this for setup, approve, deposit, withdraw, redeem, and order jobs that have not reached a terminal state.

## Safety Notes

- Prices are 0-1 floats. Treat `--price 1` as suspicious unless the user explicitly confirms.
- Trades are signed by the deposit wallet address shown by `mm predict balance`, not necessarily the connected owner EOA.
- Always inspect the market to map the user's intended outcome to the correct token ID.
