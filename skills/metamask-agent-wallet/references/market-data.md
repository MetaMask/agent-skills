# Market Data Commands

Use `price` and `token` commands for read-only token metadata, token discovery, and price data.

## `price spot` Command

Fetch spot prices for one or more CAIP-19 assets.

### Syntax

```bash
mm-dev price spot --asset-ids <asset-ids> [--vs <currency>] [--market-data]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--asset-ids` | Yes | Comma-separated CAIP-19 asset IDs |
| `--vs` | No | Quote currency; defaults to `usd` |
| `--market-data` | No | Include market cap, supply, and change percent |

### Example

```bash
mm-dev price spot --asset-ids "eip155:1/slip44:60,eip155:137/slip44:966"
mm-dev price spot --asset-ids "eip155:1/slip44:60" --vs eur
mm-dev price spot --asset-ids "eip155:1/slip44:60" --market-data
```

## `price history` Command

Fetch historical prices for an asset.

### Syntax

```bash
mm-dev price history --chain-id <caip2-chain-id> --asset-type <asset-type> [--time-period <period>] [--interval <interval>] [--from <unix>] [--to <unix>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--chain-id` | Yes | CAIP-2 chain ID |
| `--asset-type` | Yes | Asset type, such as `slip44:60` |
| `--time-period` | No | Period such as `1d`, `7d`, `2M`, or `3y` |
| `--interval` | No | `5m`, `hourly`, or `daily` |
| `--from` | No | Start unix timestamp |
| `--to` | No | End unix timestamp |

### Example

```bash
mm-dev price history --chain-id eip155:1 --asset-type slip44:60 --time-period 7d --interval daily
```

## `price currencies` Command

List supported quote currencies.

### Syntax

```bash
mm-dev price currencies
```

### Example

```bash
mm-dev price currencies
```

## `price networks` Command

List CAIP-2 networks supported by the price API.

### Syntax

```bash
mm-dev price networks
```

### Example

```bash
mm-dev price networks
```

## `token list` Commands

List popular, trending, or top-gainer tokens.

### Syntax

```bash
mm-dev token list popular --chain <chain>
mm-dev token list trending --chain <chain>
mm-dev token list top-gainer --chain <chain>
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--chain` | Yes | Chain id, CAIP-2 id, or configured chain key |

### Example

```bash
mm-dev token list popular --chain 1
mm-dev token list trending --chain 1
mm-dev token list top-gainer --chain 1
```

## `token list search` Command

Search tokens by query.

### Syntax

```bash
mm-dev token list search --query <query> [--chain <chains>] [--limit <n>] [--after <cursor>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--query` | Yes | Search query |
| `--chain` | No | Chain id, CAIP-2 id, or configured chain key |
| `--limit` | No | Maximum results |
| `--after` | No | Pagination cursor |

### Example

```bash
mm-dev token list search --query USDC --chain 1,137 --limit 25
mm-dev token list search --query WETH --chain eip155:8453
```

## `token networks` Command

List networks supported by token APIs.

### Syntax

```bash
mm-dev token networks
```

### Example

```bash
mm-dev token networks
```

## `token assets` Command

Fetch asset metadata for one or more CAIP-19 assets.

### Syntax

```bash
mm-dev token assets --asset-ids <asset-ids> [--include-market-data] [--include-token-security-data] [--include-labels]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--asset-ids` | Yes | Comma-separated CAIP-19 asset IDs |
| `--include-market-data` | No | Include market data |
| `--include-token-security-data` | No | Include token security signals |
| `--include-labels` | No | Include token labels |

### Example

```bash
mm-dev token assets --asset-ids "eip155:1/erc20:0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48,eip155:137/slip44:966"
mm-dev token assets --asset-ids "eip155:1/erc20:0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48" --include-market-data --include-token-security-data --include-labels
```
