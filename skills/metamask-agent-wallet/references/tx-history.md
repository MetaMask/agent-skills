# Transaction Commands

Use `mm tx` to look up a transaction by hash, or `mm tx history` to list recent transactions for the active wallet or specific addresses.

## `tx` command

Look up a transaction by hash.

### Syntax

```bash
mm tx --hash <hash> [--chain-id <chain-id-or-caip2>]
```

### Supported flags

| Name | Required | Description |
| --- | --- | --- |
| `--hash` | Yes | 0x-prefixed transaction hash |
| `--chain-id` | No | Chain ID or CAIP-2, such as `1` or `eip155:1`. When omitted, common EVM chains are probed |

### Example

```bash
mm tx --hash 0xabc123...
mm tx --hash 0xabc123... --chain-id 137
mm tx --hash 0xabc123... --chain-id eip155:1
```

## `tx history` command

### Syntax

```bash
mm tx history [--addresses <addrs>] [--chain-ids <chains>] [--type <filter>] [--limit <n>]
```

### Supported flags

| Name | Required | Description |
| --- | --- | --- |
| `--addresses` | No | Comma-separated EVM wallet addresses to include. Defaults to all EVM wallets for your account |
| `--chain-ids` | No | Comma-separated chain filters, such as `1,137` or `eip155:1`. Run `mm chains list` to see options |
| `--type` | No | Filter by direction: `in`, `out`, or `self`, or by transaction category/type |
| `--limit` | No | Maximum number of transactions to return, 1-500. Default 50 |

### Example

```bash
mm tx history
mm tx history --limit 10 --toon
mm tx history --chain-ids 1,8453
mm tx history --type out
mm tx history --addresses 0x742d...f2bD18 --chain-ids 137 --limit 100
```

### Output

Each history row includes enriched metadata:

| Field | Description |
| --- | --- |
| `chainName` | Human-readable chain name, such as "Ethereum" or "Polygon" |
| `chainId` | Numeric chain ID, such as 1 or 137 |
| `explorerUrl` | Block explorer link to the transaction |
| `protocol` | Protocol metadata when available, such as "swap", "transfer", or "earn" |

When a pending CLI job matches an indexed transaction hash, the original CLI intent is preserved in the output.

### Notes

- If you omit `--addresses`, the command queries all EVM wallets for your account.
- Addresses must be 0x-prefixed EVM addresses.
- `--limit` must be between 1 and 500. Values outside this range return an `INVALID_LIMIT` error.
- If your account has no EVM wallets, the command returns a `NO_HISTORY_WALLETS` error.
