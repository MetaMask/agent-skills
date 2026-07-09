# mm swap

Same-chain token swaps and cross-chain bridges. Same commands for both: when `--from-chain`
and `--to-chain` differ, the CLI routes through a bridge.

## Prerequisites

- `mm doctor` reports `authenticated: true` and `initialized: true` (SKILL.md § Preflight).
- If the user did not name a chain, ask — do not guess. Discover chain IDs with `mm chains list`.
- Amounts in quote output (`srcAssetAmount`, `destAssetAmount`, `minDestAssetAmount`, fee
  `amount`) are ATOMIC units — divide by `10^decimals` of the matching asset before showing
  them to the user. The `--amount` input flag stays human-readable.
- Multi-step patterns: workflows/swap.md (same-chain), workflows/bridge.md (cross-chain).

## mm swap quote

Get a swap or bridge quote showing expected output, fees, and route. Read-only.

### Syntax

```bash
mm swap quote --from <token> --to <token> --amount <amount> --from-chain <chain-id> [--to-chain <chain-id>] [--slippage <percent>] [--to-address <address>] [--refuel]
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--from` | token symbol | Source token symbol (`ETH`, `POL`, `USDC`) |
| `--to` | token symbol | Destination token symbol (`USDC`, `USDT`) |
| `--amount` | decimal `^\d+\.?\d*$`, > 0 | Human-readable amount to swap (`0.5`, `100`). Not wei. |
| `--from-chain` | integer `^\d+$` | Source EVM chain ID (`1` = Ethereum, `137` = Polygon) |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--to-chain` | same as `--from-chain` | integer `^\d+$` | Destination chain ID. Different value = cross-chain bridge |
| `--slippage` | `0.5` | decimal 0–100 | Maximum slippage percent. Warn the user above 1% |
| `--to-address` | active wallet | `^0x[0-9a-fA-F]{40}$` | Recipient of bridged output. Cross-chain only — rejected same-chain |
| `--refuel` | off | boolean flag | Bundle a destination native-gas top-up. Cross-chain only; best-effort (falls back to a regular quote if no aggregator offers it). Do not use when `--to` is the destination chain's native gas asset — that route returns `NO_QUOTES` |

Global flags apply — see SKILL.md § Global flags.

### Output

```json
{
  "ok": true,
  "data": {
    "quoteId": "0x20a57409b6f9702cd1919983ec7a480b6e20e70d22e9af051c9622f7ab50f2e4",
    "request": {
      "walletAddress": "0x7c2b3e65ef2b18235e2d24266f92854a70207483",
      "srcChainId": 1, "destChainId": 1,
      "srcAsset": {"symbol": "ETH", "decimals": 18},
      "destAsset": {"symbol": "USDC", "decimals": 6},
      "srcAssetAmount": "1000000000000000000",
      "slippage": 0.5
    },
    "quote": {
      "bridgeId": "okx",
      "srcAssetAmount": "991250000000000000",
      "destAssetAmount": "1724960864",
      "minDestAssetAmount": "1716336059",
      "feeData": {"metabridge": {"amount": "8750000000000000", "usd": "15.24…"}}
    }
  }
}
```

All `*AssetAmount` and fee `amount` values are atomic units — scale by each asset's
`decimals` before display (here `destAssetAmount` 1724960864 / 10^6 = 1724.96 USDC).
When a refuel-bearing quote is selected, the quote includes a `refuel` step and the
resolved request shows `refuel: true`.

Capture: `quoteId` → use as `<quote-id>` in `mm swap execute` and `mm swap status`.

### Examples

```bash
# Same-chain swap quote: 1 ETH -> USDC on Ethereum
mm swap quote --from ETH --to USDC --amount 1 --from-chain 1 --toon
# Cross-chain bridge quote: 100 USDC Ethereum -> Polygon, 1% slippage
mm swap quote --from USDC --to USDC --amount 100 --from-chain 1 --to-chain 137 --slippage 1 --toon
# Bridge to another recipient with destination gas top-up
mm swap quote --from USDC --to USDC --amount 50 --from-chain 1 --to-chain 42161 --to-address 0x742d35Cc6634C0532925a3b844Bc454e4438f44e --refuel --toon
```

## mm swap execute

Execute a swap or bridge. State-changing.

Two disjoint modes — choose exactly one:

- If the user reviewed a quote from `mm swap quote` → use mode A (`--quote-id`). Always prefer this.
- If the user explicitly waived quote review and asked for immediate execution → mode B (re-quote and execute). Otherwise never use mode B: it executes a price the user never saw.

### Mode A: execute a reviewed quote (preferred)

#### Syntax

```bash
mm swap execute --quote-id <quote-id>
```

| Flag | Value format | Description |
| --- | --- | --- |
| `--quote-id` | string from `mm swap quote` | The reviewed quote to execute. A persisted quote retains its recipient and refuel setting |

When `--quote-id` is given, all re-quote flags are ignored.

### Mode B: re-quote and execute (only on explicit user request)

#### Syntax

```bash
mm swap execute --from <token> --to <token> --amount <amount> --from-chain <chain-id> [--to-chain <chain-id>] [--slippage <percent>] [--to-address <address>] [--refuel]
```

Required: `--from`, `--to`, `--amount`, `--from-chain`. Optional: `--to-chain`, `--slippage`,
`--to-address`, `--refuel` — same formats and same cross-chain-only rules as `mm swap quote`.

Global flags and `--wallet-timeout` apply — see SKILL.md § Global flags. BYOK with an encrypted
mnemonic: set `MM_PASSWORD` first (references/concepts.md).

### Output

```json
{"ok": true, "data": {"pollingId": "...", "quoteId": "...", "txHash": "..."}}
```
<!-- shape from CLI flag metadata; not a captured run -->

Capture: `quoteId` → use as `<quote-id>` in `mm swap status --quote-id <quote-id>`.

### Async

Execution creates a wallet job (`pollingId`) — track via references/wallet-requests.md and show the
job's `intent` to the user. Then poll `mm swap status --quote-id <quote-id>` until terminal.

### Confirm before executing

Show the user ALL of: from token, to token, amount, source chain, destination chain (if
cross-chain), slippage, expected output (`destAssetAmount` scaled by decimals), minimum
received (`minDestAssetAmount` scaled), fees, recipient (if `--to-address`), destination gas
top-up (if `--refuel`). Do not run until the user approves.

### Examples

```bash
# Mode A: execute the reviewed quote
mm swap execute --quote-id 0x20a57409b6f9702cd1919983ec7a480b6e20e70d22e9af051c9622f7ab50f2e4 --toon
# Mode B (user explicitly waived quote review): swap 0.5 ETH -> USDC on Ethereum
mm swap execute --from ETH --to USDC --amount 0.5 --from-chain 1 --toon
```

## mm swap status

Check the status of a previously executed swap or bridge by its quote ID. Read-only.

### Syntax

```bash
mm swap status --quote-id <quote-id> [--tx-hash <tx-hash>]
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--quote-id` | string from `mm swap quote` | Quote that was executed |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--tx-hash` | stored hash from execute | `^0x[0-9a-fA-F]{64}$` | Source transaction hash override |

Global flags apply — see SKILL.md § Global flags.

### Output

```json
{"ok": true, "data": {"status": "...", "srcTxHash": "...", "destTxHash": "..."}}
```
<!-- shape from CLI flag metadata; not a captured run -->

Repeat until the status is terminal (completed or failed). Bridges: the destination side can
lag well behind the source transaction.

### Examples

```bash
mm swap status --quote-id 0x20a57409b6f9702cd1919983ec7a480b6e20e70d22e9af051c9622f7ab50f2e4 --toon
```

## Errors

| Code | Cause | Recovery |
| --- | --- | --- |
| `NO_QUOTES` | No route for this pair/amount; or `--refuel` used with a native-gas destination token | Try another amount/pair; verify the token exists on the chain (`mm token list search`); if `--refuel` was set, re-quote without it |
| `INVALID_SWAP_PARAMS` | `--to-address is not supported for same-chain swaps; output always goes to your wallet.` | Omit `--to-address`, or use a cross-chain swap (different `--from-chain` and `--to-chain`) to redirect output |
| `MISSING_QUOTE_ID` / `MISSING_SWAP_PARAMS` | Neither `--quote-id` nor the full re-quote flag set was provided | Provide `--quote-id`, or all of `--from --to --amount --from-chain` |
| `QUOTE_NOT_FOUND` | Quote ID expired or unknown | Re-run `mm swap quote`, re-confirm with the user, execute the new ID |
| `NATIVE_ASSET_UNSUPPORTED` | Native asset not supported for this swap route | Use the wrapped token or another pair |
| `EXECUTE_FAILED` | Swap execution failed (e.g. insufficient balance or gas) | Check `mm wallet balance --chain <chain-id>`; re-quote and retry |
| `STATUS_UNAVAILABLE` | Status backend temporarily unavailable | Retry `mm swap status` after a short delay |

Full code list: references/errors.md.
