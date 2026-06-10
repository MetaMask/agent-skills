# Predict Commands

Use the `predict` commands to trade on prediction markets (Polymarket via the CLOB).

## `predict mode` Command

Choose or display the current Predict trading mode.

### Syntax

```bash
mm predict mode [mainnet|testnet]
```

### Example

```bash
mm predict mode mainnet
mm predict mode testnet
mm predict mode
```

## `predict setup` Command

One-time Predict setup: creates trading credentials, deploys the deposit wallet, and sets approvals.

### Syntax

```bash
mm predict setup [--wait] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--wait` | No | Block until the job completes |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm predict setup --wait
```

## `predict auth` Command

Create or refresh Predict trading credentials (API key + CLOB signing).

### Syntax

```bash
mm predict auth [--refresh] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--refresh` | No | Force-create or refresh trading credentials |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm predict auth
mm predict auth --refresh
```

## `predict approve` Command

Repair missing deposit-wallet approvals.

### Syntax

```bash
mm predict approve [--wait] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--wait` | No | Block until the job completes |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm predict approve --wait
```

## `predict status` Command

Probe Predict back-end reachability (Gamma + CLOB) and report account setup status: deposit wallet address, on-chain deployment, stored CLOB credentials, and a `setupComplete` flag. 

### Syntax

```bash
mm predict status
```

### Example

```bash
mm predict status
```

## `predict geoblock` Command

Check whether Polymarket access is geoblocked for your current IP. Returns `blocked`, `ip`, `country`, and `region`.

### Syntax

```bash
mm predict geoblock
```

### Example

```bash
mm predict geoblock
```

## `predict markets list` Command

List tradeable Predict markets with Gamma-style filters.

### Syntax

```bash
mm predict markets list [--slug <slug>] [--limit <n>] [--offset <n>] [--order <fields>] [--ascending] [--tag <tag>] [--liquidity-num-min <n>] [--liquidity-num-max <n>] [--volume-num-min <n>] [--volume-num-max <n>] [--start-date-min <datetime>] [--start-date-max <datetime>] [--end-date-min <datetime>] [--end-date-max <datetime>] [--active] [--closed]
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
mm predict markets list --slug will-this-work --limit 5
mm predict markets list --tag sports --liquidity-num-min 10000 --limit 10
mm predict markets list --active --limit 50
```

## `predict markets search` Command

Search Predict markets with Polymarket public search.

### Syntax

```bash
mm predict markets search <query> [--limit <n>] [--page <n>] [--sort <field>] [--ascending] [--search-tags] [--events-status] [--recurrence <recurrence>]
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
mm predict markets search "Knicks NBA Finals" --limit 5
mm predict markets search "election" --limit 5
```

## `predict markets get` Command

Inspect a specific market and show outcome token IDs needed for quoting and placing orders.

### Syntax

```bash
mm predict markets get <market> [--market <market>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `<market>` | Yes | Market slug, ID, or condition ID (positional). Run `mm predict markets search` or `mm predict markets list` to find markets |
| `--market` | No | Same as positional `<market>` |

### Example

```bash
mm predict markets get will-the-new-york-knicks-win-the-2026-nba-finals
mm predict markets get 0x713641f745d71f6ec61f906237ffca3c8583f251e49384429a63ceb0ccdb2d37
```

## `predict events list` Command

List Polymarket events (groupings of related markets) with Gamma-style filters.

### Syntax

```bash
mm predict events list [--tag-slug <slug>] [--tag-id <n>] [--active] [--closed] [--featured] [--order <field>] [--ascending] [--liquidity-min <n>] [--start-date-min <datetime>] [--start-date-max <datetime>] [--end-date-min <datetime>] [--end-date-max <datetime>] [--limit <n>] [--offset <n>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--tag-slug` | No | Filter by tag slug (e.g. sports, politics) |
| `--tag-id` | No | Filter by tag ID (from `mm predict tags list`) |
| `--active` | No | Active events only |
| `--closed` | No | Include closed/resolved events |
| `--featured` | No | Only featured/trending events |
| `--order` | No | Sort field: `volume_24hr`, `volume`, `liquidity`, `start_date`, `end_date` |
| `--ascending` | No | Sort ascending (defaults to descending) |
| `--liquidity-min` | No | Minimum event liquidity |
| `--start-date-min` | No | Minimum event start date-time |
| `--start-date-max` | No | Maximum event start date-time |
| `--end-date-min` | No | Minimum event end date-time |
| `--end-date-max` | No | Maximum event end date-time |
| `--limit` | No | Maximum events to return, 1-500 |
| `--offset` | No | Result offset (0-based) |

### Example

```bash
mm predict events list --tag-slug sports --limit 10
mm predict events list --active --featured
```

## `predict events get` Command

Inspect a single Polymarket event by slug or ID.

### Syntax

```bash
mm predict events get <event>
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `<event>` | Yes | Event slug or ID (positional) |

### Example

```bash
mm predict events get some-event-slug
```

## `predict series list` Command

List Polymarket event series (recurring groupings of events).

### Syntax

```bash
mm predict series list [--recurrence <recurrence>] [--active] [--featured] [--tag-slug <slug>] [--limit <n>] [--offset <n>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--recurrence` | No | Filter by recurrence: `annual`, `daily`, `weekly`, or `monthly` |
| `--active` | No | Active series only |
| `--featured` | No | Only featured series |
| `--tag-slug` | No | Filter by tag slug |
| `--limit` | No | Maximum series to return, 1-500 |
| `--offset` | No | Result offset (0-based) |

### Example

```bash
mm predict series list --recurrence weekly --limit 10
```

## `predict series get` Command

Inspect a single event series by ID.

### Syntax

```bash
mm predict series get <id>
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `<id>` | Yes | Series ID (positional) |

### Example

```bash
mm predict series get 12345
```

## `predict tags list` Command

List Polymarket tags, useful for `--tag-slug` / `--tag-id` filters on events and markets.

### Syntax

```bash
mm predict tags list [--limit <n>] [--offset <n>] [--is-carousel]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--limit` | No | Maximum tags to return, 1-500 |
| `--offset` | No | Result offset (0-based) |
| `--is-carousel` | No | Only carousel tags |

### Example

```bash
mm predict tags list --limit 50
```

## `predict tags get` Command

Fetch a single Polymarket tag by numeric ID or slug.

### Syntax

```bash
mm predict tags get <tag>
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `<tag>` | Yes | Tag ID (integer) or slug string (positional) |

### Example

```bash
mm predict tags get sports
mm predict tags get 100
```

## `predict quote` Command

Preview order cost and fill before placing.

### Syntax

```bash
mm predict quote <token-id> [--token-id <token-id>] --side <side> --size <size> [--limit-price <price>] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `<token-id>` | Yes | Outcome token ID (positional). Run `mm predict markets get <slug>` to get token IDs |
| `--token-id` | No | Same as positional `<token-id>` |
| `--side` | Yes | Order side: `buy` or `sell` |
| `--size` | Yes | Order size in shares, human-readable (e.g. 1, 100) |
| `--limit-price` | No | Execution price per share, between 0 and 1 |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm predict quote --token-id <token-id> --side buy --size 1
mm predict quote --token-id <token-id> --side sell --size 5 --limit-price 0.60
```

## `predict place` Command

Place a Predict order (GTC/GTD limit, FOK/FAK market).

### Syntax

```bash
mm predict place <token-id> [--token-id <token-id>] --side <side> --size <size> --price <price> [--order-type <type>] [--post-only] [--expiration <unix>] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `<token-id>` | Yes | Outcome token ID (positional). Run `mm predict markets get <slug>` to get token IDs |
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
mm predict place --token-id <token-id> --side buy --size 1 --price 0.80
mm predict place --token-id <token-id> --side buy --size 5 --price 1 --order-type FOK
mm predict place --token-id <token-id> --side sell --size 2 --price 0.7 --order-type GTD --expiration 1735689600
```

## `predict cancel` Command

Cancel Predict orders by ID, market, asset, or all open orders.

### Syntax

```bash
mm predict cancel [<order-id>] [--order-id <id>] [--all] [--market <condition-id>] [--asset <token-id>] [--password <password>]
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
mm predict cancel <order-id>
mm predict cancel --order-id <order-id>
mm predict cancel --all
mm predict cancel --market <condition-id>
mm predict cancel --asset <token-id>
```

## `predict positions` Command

View your Predict positions.

### Syntax

```bash
mm predict positions [--market <id>] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--market` | No | Market slug, ID, or condition ID. Run `mm predict markets search` or `mm predict markets list` to find markets |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm predict positions
mm predict positions --market <condition-id>
```

## `predict portfolio` Command

Full portfolio snapshot: deposit wallet pUSD balance, open positions with estimated value, and outstanding redeemable winnings.

### Syntax

```bash
mm predict portfolio [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm predict portfolio
```

## `predict redeem list` Command

List all redeemable (winning) positions in your deposit wallet, with position size and market question.

### Syntax

```bash
mm predict redeem list [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm predict redeem list
```

## `predict redeem` Command

Redeem winning tokens after market resolution. Redeem one position by condition ID, or all redeemable positions with `--all`. With `--wait`, polls for the transaction receipt.

### Syntax

```bash
mm predict redeem [<condition-id>] [--all] [--wait] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `<condition-id>` | Yes (unless `--all`) | Market condition ID to redeem (positional) |
| `--all` | No | Redeem all redeemable positions |
| `--wait` | No | Block until the redemption transaction is confirmed |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Validation Rules

- Provide either a `<condition-id>` or `--all`, not both.

### Example

```bash
mm predict redeem 0xABC123... --wait
mm predict redeem --all --wait
```

## `predict orders` Command

View open Predict orders.

### Syntax

```bash
mm predict orders [--market <condition-id>] [--cursor <cursor>] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--market` | No | Market slug, ID, or condition ID. Run `mm predict markets search` or `mm predict markets list` to find markets |
| `--cursor` | No | Pagination cursor from a previous response |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm predict orders
mm predict orders --market <condition-id>
```

## `predict balance` Command

Check deposit wallet funds, approvals, and setup status.

### Syntax

```bash
mm predict balance [--token-id <token-id>] [--sync] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--token-id` | No | Outcome token ID. Run `mm predict markets get <slug>` to get token IDs |
| `--sync` | No | Refresh balances and allowances before reading |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm predict balance --sync
mm predict balance --token-id <token-id> --sync
```

## `predict withdraw` Command

Withdraw pUSD from your Predict deposit wallet to your owner EOA or another address. Validates the amount against the on-chain deposit wallet balance before signing. Uses the Polymarket Relayer batch mechanism.

### Syntax

```bash
mm predict withdraw --amount <amount> [--to <address>] [--wait] [--password <password>]
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
mm predict withdraw --amount 10 --wait
mm predict withdraw --amount 5 --to 0xAbc... --wait
```

## `predict deposit` Command

Convert USDC.e from your EOA to pUSD in your Predict deposit wallet.

### Syntax

```bash
mm predict deposit --amount <amount> [--wait] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--amount` | Yes | pUSD amount to deposit, human-readable (e.g. 5, 100) |
| `--wait` | No | Block until the job completes |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm predict deposit --amount 5 --wait
```

## `predict book` Command

Fetch the raw order book for an outcome token.

### Syntax

```bash
mm predict book <token-id> [--token-id <token-id>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `<token-id>` | Yes | Outcome token ID (positional). Run `mm predict markets get <slug>` to get token IDs |
| `--token-id` | No | Same as positional `<token-id>` |

### Example

```bash
mm predict book --token-id <token-id>
```

## `predict watch` Command

Watch a setup, approval, deposit, withdraw, or order job until it completes.

### Syntax

```bash
mm predict watch <id> [--id <id>] [--wait] [--password <password>]
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
mm predict watch <job-id> --wait
mm predict watch --id <job-id> --wait
```

## Notes

- Before trading, run `mm predict setup --wait` to initialize credentials, deploy the deposit wallet, and set approvals.
- `mm predict setup` aborts early with `PREDICT_GEOBLOCKED` if your IP resolves to a restricted region, before any wallet interaction. Use `mm predict geoblock` to check region status without running setup.
- Use `mm predict markets get <slug>` to get outcome token IDs required by `quote`, `place`, `book`, and `balance --token-id`.
- Use `mm predict events`, `mm predict series`, and `mm predict tags` to browse Polymarket content; tag slugs/IDs from `mm predict tags list` feed the `--tag-slug` / `--tag-id` filters on `events` and `markets`.
- After a market resolves, use `mm predict redeem list` to see winnings and `mm predict redeem <condition-id> --wait` (or `--all`) to claim them. `mm predict portfolio` shows balance, open positions, and redeemable winnings in one snapshot.
- Prices are per-share and must be in the range [0, 1].
- Side must be `buy` or `sell`.
- The `predict mode` command switches between `mainnet` and `testnet`.
- If the user does not specify a mode, the CLI uses the previously set mode.
- Setup, approve, deposit, withdraw, redeem, and order flows can return job IDs. Track them with `mm predict watch <job-id> --wait`.
