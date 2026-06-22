# Swap & Bridge Commands

Use the `swap` commands to perform same-chain token swaps or cross-chain bridges. When `--from-chain` and `--to-chain` differ, the CLI automatically routes through a bridge.

## `swap quote` Command

Get a swap or bridge quote showing expected output, fees, and route.

### Syntax

```bash
mm swap quote --from <token> --to <token> --amount <amount> --from-chain <chain-id> [--to-chain <chain-id>] [--to-address <address>] [--slippage <percent>] [--refuel]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--from` | Yes | Source token symbol (e.g. ETH, POL, USDC) |
| `--to` | Yes | Destination token symbol (e.g. USDC, USDT) |
| `--amount` | Yes | Human-readable amount to swap (e.g. 0.5, 100) |
| `--from-chain` | Yes | Source EVM chain ID (e.g. 1 for Ethereum, 137 for Polygon) |
| `--to-chain` | No | Destination EVM chain ID. Defaults to `--from-chain` for same-chain swaps |
| `--to-address` | No | Recipient address for bridged output tokens. Only valid for cross-chain swaps. Defaults to the signer's wallet |
| `--slippage` | No | Maximum slippage as a percentage, 0-100 (defaults to 0.5) |
| `--refuel` | No | Bundle a small destination native-gas top-up into a cross-chain quote. Only valid when `--to-chain` differs from `--from-chain`. See [Refuel](#refuel) |

### Example

```bash
mm swap quote --from ETH --to USDC --amount 0.5 --from-chain 1
mm swap quote --from USDC --to USDT --amount 100 --from-chain 137
mm swap quote --from ETH --to USDC --amount 1 --from-chain 1 --to-chain 137
mm swap quote --from ETH --to USDC --amount 0.5 --from-chain 1 --slippage 1
mm swap quote --from ETH --to pUSD --amount 0.5 --from-chain 1 --to-chain 137 --to-address 0x742d...f2bD18
mm swap quote --from ETH --to USDC --amount 1 --from-chain 1 --to-chain 42161 --refuel
```

## `swap execute` Command

Execute a swap or bridge, either by referencing a previous quote ID or by providing parameters for an automatic re-quote and execute.

### Syntax

```bash
mm swap execute --quote-id <id> [--password <password>]
mm swap execute --from <token> --to <token> --amount <amount> --from-chain <chain-id> [--to-chain <chain-id>] [--to-address <address>] [--slippage <percent>] [--refuel] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--quote-id` | Yes (unless re-quote args given) | Quote ID returned by `mm swap quote`. If omitted, provide `--from`, `--to`, `--amount`, and `--from-chain` to re-quote |
| `--from` | Yes (unless `--quote-id`) | Source token symbol |
| `--to` | Yes (unless `--quote-id`) | Destination token symbol |
| `--amount` | Yes (unless `--quote-id`) | Amount to swap |
| `--from-chain` | Yes (unless `--quote-id`) | Source EVM chain ID |
| `--to-chain` | No | Destination EVM chain ID. Defaults to `--from-chain` for same-chain swaps |
| `--to-address` | No | Recipient address for bridged output tokens. Only valid for cross-chain swaps. Defaults to the signer's wallet. Persisted quotes retain the recipient for `--quote-id` execution |
| `--slippage` | No | Maximum slippage as a percentage, 0-100 (defaults to 0.5) |
| `--refuel` | No | Bundle a destination native-gas top-up into a cross-chain re-quote. Only valid when `--to-chain` differs from `--from-chain`; ignored when executing by `--quote-id` (the persisted quote already carries the flag). See [Refuel](#refuel) |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

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
| `--quote-id` | Yes | Quote ID returned by `mm swap quote` |
| `--tx-hash` | No | Source transaction hash. Overrides the stored hash from execute |

### Example

```bash
mm swap status --quote-id <quote-id>
mm swap status --quote-id <quote-id> --tx-hash 0xabc...123
```

## Refuel

Refuel bundles a small amount of the **destination chain's native gas token** into a cross-chain quote, so the recipient lands with gas to spend even if they arrive with a zero native balance. This is useful when bridging to a chain where the recipient holds none of the gas token (e.g. bridging USDC to Arbitrum with no ETH there).

- **Opt-in only.** Refuel is never enabled automatically — pass `--refuel` to request it.
- **Cross-chain only.** `--refuel` is only meaningful when `--to-chain` differs from `--from-chain`. It has no effect on same-chain swaps.
- **Not for native-asset destinations.** Do not use `--refuel` when the destination token is the destination chain's native gas asset (e.g. bridging ETH from Base into ETH on Arbitrum). There is nothing to top up, and the backend returns **0 quotes** for the route — surfaced as a `NO_QUOTES` error. Only use `--refuel` when bridging into a non-native token (e.g. USDC).
- **Best-effort.** Only some bridge aggregators offer a gas top-up. When `--refuel` is set, the CLI prefers a quote that includes the top-up; if no aggregator offers one for that route, it falls back to the best regular quote (no error).
- **Output.** When a refuel-bearing quote is selected, the quote includes a `refuel` step describing the native-gas top-up (source amount spent and destination native amount received), and the resolved request shows `refuel: true`.

```bash
# Bridge USDC to Arbitrum and top up ETH for gas on arrival
mm swap quote --from USDC --to USDC --amount 50 --from-chain 1 --to-chain 42161 --refuel
```

## Notes

- If the chain is not mentioned by the user, ask for the chain.
- Use `mm chains list` to discover supported chain IDs.
- Same-chain swap: omit `--to-chain` (it defaults to `--from-chain`).
- Cross-chain bridge: set `--to-chain` to a different chain than `--from-chain`. The CLI automatically routes through a bridge.
- The typical flow is: `mm swap quote` to preview, then `mm swap execute --quote-id <id>` to submit.
- You can skip the quote step by passing all swap parameters directly to `mm swap execute`.
- Use `mm swap status --quote-id <id>` to track progress after execution.
- If the user asks to "bridge" tokens, use the `swap` commands with different `--from-chain` and `--to-chain` values.
- If the user is bridging to a chain where they hold no native gas token, suggest `--refuel` to top up gas on the destination (cross-chain only). See [Refuel](#refuel).
- After execution, track swap progress with `mm swap status --quote-id <id>`.
