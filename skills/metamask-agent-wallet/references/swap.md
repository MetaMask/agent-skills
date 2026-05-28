# Swap & Bridge Commands

Use the `swap` commands to perform same-chain token swaps or cross-chain bridges. When `--from-chain` and `--to-chain` differ, the CLI automatically routes through a bridge.

## `swap quote` Command

Get a swap or bridge quote showing expected output, fees, and route.

### Syntax

```bash
mm swap quote --from <token> --to <token> --amount <amount> --from-chain <chain-id> [--to-chain <chain-id>] [--slippage <percent>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--from` | Yes | Source token symbol (e.g. ETH, POL, USDC) |
| `--to` | Yes | Destination token symbol (e.g. USDC, USDT) |
| `--amount` | Yes | Amount to swap |
| `--from-chain` | Yes | Source EVM chain ID (e.g. 1 for Ethereum, 137 for Polygon) |
| `--to-chain` | No | Destination EVM chain ID; defaults to `--from-chain` (same-chain swap). Set a different chain to bridge |
| `--slippage` | No | Max slippage percent (e.g. 0.5); defaults to 0.5 |

### Example

```bash
mm swap quote --from ETH --to USDC --amount 0.5 --from-chain 1
mm swap quote --from USDC --to USDT --amount 100 --from-chain 137
mm swap quote --from ETH --to USDC --amount 1 --from-chain 1 --to-chain 137
mm swap quote --from ETH --to USDC --amount 0.5 --from-chain 1 --slippage 1
```

## `swap execute` Command

Execute a swap or bridge, either by referencing a previous quote ID or by providing parameters for an automatic re-quote and execute.

### Syntax

```bash
mm swap execute --quote-id <id>
mm swap execute --from <token> --to <token> --amount <amount> --from-chain <chain-id> [--to-chain <chain-id>] [--slippage <percent>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--quote-id` | Yes (unless re-quote args given) | Quote ID from a previous `mm swap quote` |
| `--from` | Yes (unless `--quote-id`) | Source token symbol |
| `--to` | Yes (unless `--quote-id`) | Destination token symbol |
| `--amount` | Yes (unless `--quote-id`) | Amount to swap |
| `--from-chain` | Yes (unless `--quote-id`) | Source EVM chain ID |
| `--to-chain` | No | Destination EVM chain ID; defaults to `--from-chain` |
| `--slippage` | No | Max slippage percent; defaults to 0.5 |

### Validation Rules

- Either `--quote-id` OR the full set of re-quote flags (`--from`, `--to`, `--amount`, `--from-chain`) must be provided.
- When `--quote-id` is given, re-quote flags are ignored.

### Example

```bash
mm swap execute --quote-id <quote-id>
mm swap execute --from ETH --to USDC --amount 0.5 --from-chain 1
mm swap execute --from USDC --to USDT --amount 100 --from-chain 137 --to-chain 137 --slippage 1
```

## `swap status` Command

Check the status of a previously executed swap or bridge by its quote ID.

### Syntax

```bash
mm swap status --quote-id <id> [--tx-hash <hash>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--quote-id` | Yes | Quote ID from a previous swap |
| `--tx-hash` | No | Source trade transaction hash (overrides the stored hash from execute) |

### Example

```bash
mm swap status --quote-id <quote-id>
mm swap status --quote-id <quote-id> --tx-hash 0xabc...123
```

## Notes

- Use `mm chains list` to discover supported chain IDs.
- Same-chain swap: omit `--to-chain` (it defaults to `--from-chain`).
- Cross-chain bridge: set `--to-chain` to a different chain than `--from-chain`. The CLI automatically routes through a bridge.
- The typical flow is: `mm swap quote` to preview, then `mm swap execute --quote-id <id>` to submit.
- You can skip the quote step by passing all swap parameters directly to `mm swap execute`.
- Use `mm swap status --quote-id <id>` to track progress after execution.
- If the user asks to "bridge" tokens, use the `swap` commands with different `--from-chain` and `--to-chain` values.
- After execution, track swap progress with `mm swap status --quote-id <id>`.
