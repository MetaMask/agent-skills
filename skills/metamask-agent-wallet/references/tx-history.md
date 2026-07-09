# mm tx

Look up a transaction by hash and list recent transactions for your wallets.

## Prerequisites

- `mm doctor` reports `authenticated: true` and `initialized: true` (SKILL.md § Preflight).
- History covers EVM wallets in your account roster only.

## mm tx

Look up a single transaction by hash. Read-only.

### Syntax

```bash
mm tx --hash <tx-hash> [--chain <chain-id>]
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--hash` | `^0x[0-9a-fA-F]{64}$` | Transaction hash |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--chain` | probe common EVM chains | `<chain-id>` or `<caip2>` (`1` or `eip155:1`) | Chain to query; pass it when known — probing is slower |

Global flags apply — see SKILL.md § Global flags.

### Output

```
ok: true
data:
  status: success
  receipt:
    hash: 0x21333b4f532bbc967275c03c21664cc753cbd527e234d17a39134cbc19497bfa
    timestamp: "2026-06-17T15:11:47.000Z"
    chainId: 1
    blockNumber: 25338081
    gasUsed: 21000
    effectiveGasPrice: "2502497925"
    value: "4340000000000000"
    to: 0xae92af9d910e7df9914caa34936dd27beaf4220b
    from: 0x7c2b3e65ef2b18235e2d24266f92854a70207483
    isError: false
```

### Examples

```bash
mm tx --hash 0x21333b4f532bbc967275c03c21664cc753cbd527e234d17a39134cbc19497bfa --chain 1 --toon
```

## mm tx history

List recent transactions for the active wallet (or specific addresses). Read-only.

### Syntax

```bash
mm tx history [--chain <chain-id>] [--type <type>] [--limit <limit>] [--addresses <address>]
```

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--addresses` | all EVM wallets in roster | comma-separated `<address>` | Wallet addresses to include |
| `--chain` | all | comma-separated `<chain-id>` or `<caip2>` (`1,137` or `eip155:1`) | Chain filter; discover with `mm chains list` |
| `--type` | all | `in`, `out`, `self`, or a category/type | Filter by direction or transaction type |
| `--limit` | 50 | integer 1-500 | Maximum number of transactions to return |

Global flags apply — see SKILL.md § Global flags.

### Output

```
ok: true
data:
  items[3]{txHash,type,status,summary,ts}:
    0xc777ff9dcde0f2958f15d156a9695f3277121f656e16438957d93e897297fc82,TRANSFER,success,Received 1 TWT from 0x8b7e…6447,"2026-06-24T09:24:43.000Z"
    0x21333b4f532bbc967275c03c21664cc753cbd527e234d17a39134cbc19497bfa,STANDARD,success,Sent 0.00434 ETH to 0xae92…220b,"2026-06-17T15:11:47.000Z"
  unprocessedNetworks: []
  warnings: []
```

Capture: `txHash` → use as `<tx-hash>` in `mm tx --hash <tx-hash>`.

### Examples

```bash
mm tx history --limit 10 --toon
mm tx history --chain 1,8453 --type out --toon
mm tx history --addresses 0x7c2b3e65ef2b18235e2d24266f92854a70207483 --chain 137 --limit 100 --toon
```

## Errors

| Code | Cause | Recovery |
| --- | --- | --- |
| `INVALID_LIMIT` | `--limit` outside 1-500 (e.g. `0`) | Pass an integer between 1 and 500 |
| `NO_HISTORY_WALLETS` | Account has no EVM wallets in roster | Create one via references/wallet.md, then retry |
| `INVALID_CHAIN` | Unknown chain filter | Run `mm chains list` and use a listed `chainId` or `caip2` |

Full code list: references/errors.md.
