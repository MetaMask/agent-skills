# Transaction history command

Use `mm tx history` to list recent transactions for the active wallet or specific addresses.

## `tx history` command

### Syntax

```bash
mm tx history [--addresses <addrs>] [--chain <chains>] [--type <filter>] [--limit <n>]
```

### Supported flags

| Name | Required | Description |
| --- | --- | --- |
| `--addresses` | No | Comma-separated EVM wallet addresses to include. Defaults to all EVM wallets for your account |
| `--chain` | No | Comma-separated chain filters (e.g. `1,137` or `eip155:1`). Run `mm chains list` to see options |
| `--type` | No | Filter by direction (`in`, `out`, `self`) or transaction category/type |
| `--limit` | No | Maximum number of transactions to return (1-500, default 50) |

### Example

```bash
mm tx history
mm tx history --limit 10 --toon
mm tx history --chain 1,8453
mm tx history --type out
mm tx history --addresses 0x742d...f2bD18 --chain 137 --limit 100
```

### Notes

- If you omit `--addresses`, the command queries all EVM wallets for your account.
- Addresses must be 0x-prefixed EVM addresses.
- `--limit` must be between 1 and 500. Values outside this range return an `INVALID_LIMIT` error.
- If your account has no EVM wallets, the command returns a `NO_HISTORY_WALLETS` error.
