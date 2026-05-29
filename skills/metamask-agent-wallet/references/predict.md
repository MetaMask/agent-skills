# Predict Commands

Use the `predict` commands to trade on prediction markets (Polymarket via the CLOB).

**Workflow:** [predict-trading.md](../workflows/predict-trading.md) — setup, cross-chain funding, quote, place, and close.

## `predict mode` Command

Choose or display the current Predict trading mode.

### Syntax

```bash
mm-dev predict mode [mainnet|testnet]
```

### Example

```bash
mm-dev predict mode mainnet
mm-dev predict mode testnet
mm-dev predict mode
```

## `predict setup` Command

One-time Predict setup: creates trading credentials, deploys the deposit wallet, and sets approvals.

### Syntax

```bash
mm-dev predict setup [--wait] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--wait` | No | Block until the job completes |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm-dev predict setup --wait
```

## `predict auth` Command

Create or refresh Predict trading credentials (API key + CLOB signing).

### Syntax

```bash
mm-dev predict auth [--refresh] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--refresh` | No | Force-create or refresh trading credentials |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm-dev predict auth
mm-dev predict auth --refresh
```

## `predict approve` Command

Repair missing deposit-wallet approvals.

### Syntax

```bash
mm-dev predict approve [--wait] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--wait` | No | Block until the job completes |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm-dev predict approve --wait
```

## `predict status` Command

Probe Predict back-end reachability (Gamma + CLOB).

### Syntax

```bash
mm-dev predict status
```

### Example

```bash
mm-dev predict status
```

## `predict markets list` Command

List tradeable Predict markets with Gamma-style filters.

### Syntax

```bash
mm-dev predict markets list [--slug <slug>] [--limit <n>] [--offset <n>] [--order <fields>] [--ascending] [--tag <tag>] [--liquidity-num-min <n>] [--liquidity-num-max <n>] [--volume-num-min <n>] [--volume-num-max <n>] [--start-date-min <datetime>] [--start-date-max <datetime>] [--end-date-min <datetime>] [--end-date-max <datetime>] [--active] [--closed]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--slug` | No | Market slug to filter by |
| `--limit` | No | Maximum markets to return, 1-500 |
| `--offset` | No | Market result offset (0-based) |
| `--order` | No | Comma-separated market fields to order by |
| `--ascending` | No | Sort markets in ascending order |
| `--tag` | No | Market tag or category (e.g. sports, politics) |
| `--liquidity-num-min` | No | Minimum market liquidity |
| `--liquidity-num-max` | No | Maximum market liquidity |
| `--volume-num-min` | No | Minimum market volume |
| `--volume-num-max` | No | Maximum market volume |
| `--start-date-min` | No | Minimum market start date-time |
| `--start-date-max` | No | Maximum market start date-time |
| `--end-date-min` | No | Minimum market end date-time |
| `--end-date-max` | No | Maximum market end date-time |
| `--active` | No | Only include active markets |
| `--closed` | No | Include closed markets |

### Example

```bash
mm-dev predict markets list --slug will-this-work --limit 5
mm-dev predict markets list --tag sports --liquidity-num-min 10000 --limit 10
mm-dev predict markets list --active --limit 50
```

## `predict markets search` Command

Search Predict markets with Polymarket public search.

### Syntax

```bash
mm-dev predict markets search <query> [--limit <n>] [--page <n>] [--sort <field>] [--ascending] [--search-tags] [--events-status] [--recurrence <recurrence>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `<query>` | Yes | Search string (positional) |
| `--limit` | No | Results per type (defaults to 10) |
| `--page` | No | Search result page |
| `--sort` | No | Search sort field |
| `--ascending` | No | Sort search results in ascending order |
| `--search-tags` | No | Include tag matches in search results (defaults to true; use `--no-search-tags` to disable) |
| `--events-status` | No | Restrict to active events (defaults to true; use `--no-events-status` for all) |
| `--recurrence` | No | Filter by series recurrence: `daily`, `weekly`, or `monthly` |

### Example

```bash
mm-dev predict markets search "Knicks NBA Finals" --limit 5
mm-dev predict markets search "election" --limit 5
```

## `predict markets get` Command

Inspect a specific market and show outcome token IDs needed for quoting and placing orders.

### Syntax

```bash
mm-dev predict markets get <market> [--market <market>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `<market>` | Yes | Market slug, ID, or condition ID (positional). Run `mm-dev predict markets search` or `mm-dev predict markets list` to find markets |
| `--market` | No | Same as positional `<market>` |

### Example

```bash
mm-dev predict markets get will-the-new-york-knicks-win-the-2026-nba-finals
mm-dev predict markets get 0x713641f745d71f6ec61f906237ffca3c8583f251e49384429a63ceb0ccdb2d37
```

## `predict quote` Command

Preview order cost and fill before placing.

### Syntax

```bash
mm-dev predict quote <token-id> [--token-id <token-id>] --side <side> --size <size> [--limit-price <price>] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `<token-id>` | Yes | Outcome token ID (positional). Run `mm-dev predict markets get <slug>` to get token IDs |
| `--token-id` | No | Same as positional `<token-id>` |
| `--side` | Yes | Order side: `buy` or `sell` |
| `--size` | Yes | Order size in shares, human-readable (e.g. 1, 100) |
| `--limit-price` | No | Execution price per share, between 0 and 1 |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm-dev predict quote --token-id <token-id> --side buy --size 1
mm-dev predict quote --token-id <token-id> --side sell --size 5 --limit-price 0.60
```

## `predict place` Command

Place a Predict order (GTC/GTD limit, FOK/FAK market).

### Syntax

```bash
mm-dev predict place <token-id> [--token-id <token-id>] --side <side> --size <size> --price <price> [--order-type <type>] [--post-only] [--expiration <unix>] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `<token-id>` | Yes | Outcome token ID (positional). Run `mm-dev predict markets get <slug>` to get token IDs |
| `--token-id` | No | Same as positional `<token-id>` |
| `--side` | Yes | Order side: `buy` or `sell` |
| `--size` | Yes | Order size in shares, human-readable (e.g. 1, 100) |
| `--price` | Yes | Worst price per share (0-1); limit price for GTC/GTD, worst fill for FOK/FAK |
| `--order-type` | No | Order type: `GTC`, `GTD`, `FOK`, or `FAK` (defaults to `GTC`) |
| `--post-only` | No | Reject if the order would cross the book. Not supported with FOK/FAK orders |
| `--expiration` | If `GTD` | Expiration as a Unix timestamp in seconds (only valid for GTD orders) |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Validation Rules

- `--post-only` cannot be used with FOK or FAK orders.
- `--expiration` is only valid for GTD orders.

### Example

```bash
mm-dev predict place --token-id <token-id> --side buy --size 1 --price 0.80
mm-dev predict place --token-id <token-id> --side buy --size 5 --price 1 --order-type FOK
mm-dev predict place --token-id <token-id> --side sell --size 2 --price 0.7 --order-type GTD --expiration 1735689600
```

## `predict cancel` Command

Cancel Predict orders by ID, market, asset, or all open orders.

### Syntax

```bash
mm-dev predict cancel [<order-id>] [--order-id <id>] [--all] [--market <condition-id>] [--asset <token-id>] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `<order-id>` | Yes (unless `--all`/`--market`/`--asset`) | Order ID to cancel (positional) |
| `--order-id` | No | Same as positional `<order-id>` |
| `--all` | No | Cancel all open orders |
| `--market` | No | Cancel orders for a given market condition ID |
| `--asset` | No | Cancel orders for a specific outcome token ID |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Validation Rules

- Use only one of `--order-id`, `--all`, or `--market`/`--asset` (market and asset can be combined as one target).

### Example

```bash
mm-dev predict cancel <order-id>
mm-dev predict cancel --order-id <order-id>
mm-dev predict cancel --all
mm-dev predict cancel --market <condition-id>
mm-dev predict cancel --asset <token-id>
```

## `predict positions` Command

View your Predict positions.

### Syntax

```bash
mm-dev predict positions [--market <id>] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--market` | No | Market slug, ID, or condition ID. Run `mm-dev predict markets search` or `mm-dev predict markets list` to find markets |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm-dev predict positions
mm-dev predict positions --market <condition-id>
```

## `predict orders` Command

View open Predict orders.

### Syntax

```bash
mm-dev predict orders [--market <condition-id>] [--cursor <cursor>] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--market` | No | Market slug, ID, or condition ID. Run `mm-dev predict markets search` or `mm-dev predict markets list` to find markets |
| `--cursor` | No | Pagination cursor from a previous response |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm-dev predict orders
mm-dev predict orders --market <condition-id>
```

## `predict balance` Command

Check deposit wallet funds, approvals, and setup status.

### Syntax

```bash
mm-dev predict balance [--token-id <token-id>] [--sync] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--token-id` | No | Outcome token ID. Run `mm-dev predict markets get <slug>` to get token IDs |
| `--sync` | No | Refresh balances and allowances before reading |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm-dev predict balance --sync
mm-dev predict balance --token-id <token-id> --sync
```

## `predict withdraw` Command

Withdraw pUSD from your Predict deposit wallet to your owner EOA or another address. Validates the amount against the on-chain deposit wallet balance before signing. Uses the Polymarket Relayer batch mechanism.

### Syntax

```bash
mm-dev predict withdraw --amount <amount> [--to <address>] [--wait] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--amount` | Yes | pUSD amount to withdraw, human-readable (e.g. 0.1, 5, 100) |
| `--to` | No | Recipient address. Defaults to your owner EOA |
| `--wait` | No | Block until the job completes |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm-dev predict withdraw --amount 10 --wait
mm-dev predict withdraw --amount 5 --to 0xAbc... --wait
```

## `predict deposit` Command

Convert USDC.e from your EOA to pUSD in your Predict deposit wallet.

### Syntax

```bash
mm-dev predict deposit --amount <amount> [--wait] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--amount` | Yes | pUSD amount to deposit, human-readable (e.g. 5, 100) |
| `--wait` | No | Block until the job completes |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm-dev predict deposit --amount 5 --wait
```

## `predict book` Command

Fetch the raw order book for an outcome token.

### Syntax

```bash
mm-dev predict book <token-id> [--token-id <token-id>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `<token-id>` | Yes | Outcome token ID (positional). Run `mm-dev predict markets get <slug>` to get token IDs |
| `--token-id` | No | Same as positional `<token-id>` |

### Example

```bash
mm-dev predict book --token-id <token-id>
```

## `predict watch` Command

Watch a setup, approval, deposit, withdraw, or order job until it completes.

### Syntax

```bash
mm-dev predict watch <id> [--id <id>] [--wait] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `<id>` | Yes | Job or transaction ID to watch (positional) |
| `--id` | No | Same as positional `<id>` |
| `--wait` | No | Block until the job completes |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm-dev predict watch <job-id> --wait
mm-dev predict watch --id <job-id> --wait
```

## Notes

- Before trading, run `mm-dev predict setup --wait` to initialize credentials, deploy the deposit wallet, and set approvals.
- Use `mm-dev predict markets get <slug>` to get outcome token IDs required by `quote`, `place`, `book`, and `balance --token-id`.
- Prices are per-share and must be in the range [0, 1].
- Side must be `buy` or `sell`.
- The `predict mode` command switches between `mainnet` and `testnet`.
- If the user does not specify a mode, the CLI uses the previously set mode.
- Setup, approve, deposit, withdraw, and order flows can return job IDs. Track them with `mm-dev predict watch <job-id> --wait`.
