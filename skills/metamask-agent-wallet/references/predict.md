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

Probe Predict back-end reachability (Gamma + CLOB).

### Syntax

```bash
mm predict status
```

### Example

```bash
mm predict status
```

## `predict markets` Command

Search tradeable Predict markets.

### Syntax

```bash
mm predict markets [--query <text>] [--limit <n>] [--cursor <cursor>] [--tag <tag>] [--active] [--closed]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--query` | No | Search query for market names (e.g. NBA Finals) |
| `--limit` | No | Maximum markets to return, 1-500 |
| `--cursor` | No | Pagination cursor from a previous response |
| `--tag` | No | Market tag or category (e.g. sports, politics) |
| `--active` | No | Only include active markets |
| `--closed` | No | Include closed markets |

### Example

```bash
mm predict markets --query "Knicks NBA Finals" --limit 5 --active
mm predict markets --tag sports --limit 10
```

## `predict market` Command

Inspect a specific market and show outcome token IDs needed for quoting and placing orders.

### Syntax

```bash
mm predict market <market>
```

### Supported Args

| Name | Required | Description |
| --- | --- | --- |
| `<market>` | Yes | Market slug, ID, or condition ID |

### Example

```bash
mm predict market will-the-new-york-knicks-win-the-2026-nba-finals
mm predict market 0x713641f745d71f6ec61f906237ffca3c8583f251e49384429a63ceb0ccdb2d37
```

## `predict quote` Command

Preview order cost and fill before placing.

### Syntax

```bash
mm predict quote --token-id <token-id> --side <side> --size <size> [--limit-price <price>] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--token-id` | Yes | Outcome token ID. Run `mm predict market <slug>` to get token IDs |
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
mm predict place --token-id <token-id> --side <side> --size <size> --price <price> [--order-type <type>] [--post-only] [--expiration <unix>] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--token-id` | Yes | Outcome token ID. Run `mm predict market <slug>` to get token IDs |
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
mm predict cancel [<order-id>] [--all] [--market <condition-id>] [--asset <token-id>] [--password <password>]
```

### Supported Args

| Name | Required | Description |
| --- | --- | --- |
| `<order-id>` | Yes (unless `--all`/`--market`/`--asset`) | Order ID to cancel |

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--all` | No | Cancel all open orders |
| `--market` | No | Cancel orders for a given market condition ID |
| `--asset` | No | Cancel orders for a specific outcome token ID |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Validation Rules

- Exactly one of `<order-id>`, `--all`, `--market`, or `--asset` must be provided.

### Example

```bash
mm predict cancel <order-id>
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
| `--market` | No | Market slug, ID, or condition ID. Run `mm predict markets` to search |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm predict positions
mm predict positions --market <condition-id>
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
| `--market` | No | Filter by market condition ID |
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
| `--token-id` | No | Optional conditional token ID |
| `--sync` | No | Refresh balances and allowances before reading |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm predict balance --sync
mm predict balance --token-id <token-id> --sync
```

## `predict deposit` Command

Fund your Predict deposit wallet with pUSD.

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
mm predict book <token-id>
```

### Supported Args

| Name | Required | Description |
| --- | --- | --- |
| `<token-id>` | Yes | Outcome token ID |

### Example

```bash
mm predict book <token-id>
```

## `predict watch` Command

Watch a setup, approval, deposit, or order job until it completes.

### Syntax

```bash
mm predict watch <id> [--wait] [--password <password>]
```

### Supported Args

| Name | Required | Description |
| --- | --- | --- |
| `<id>` | Yes | Setup, approval, order, or job ID |

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--wait` | No | Block until the job completes |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm predict watch <job-id> --wait
```

## Notes

- Before trading, run `mm predict setup --wait` to initialize credentials, deploy the deposit wallet, and set approvals.
- Use `mm predict market <slug>` to get outcome token IDs required by `quote`, `place`, `book`, and `balance --token-id`.
- Prices are per-share and must be in the range [0, 1].
- Side must be `buy` or `sell`.
- The `predict mode` command switches between `mainnet` and `testnet`.
- If the user does not specify a mode, the CLI uses the previously set mode.
- Setup, approve, deposit, and order flows can return job IDs. Track them with `mm predict watch <job-id> --wait`.
