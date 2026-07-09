# mm transfer

Send native or ERC-20 tokens from the active wallet to a recipient address. State-changing.

## Prerequisites

- `mm doctor` reports `authenticated: true` and `initialized: true` (SKILL.md § Preflight).
- Recipient is a full `0x` + 40-hex address. ENS names are not supported.
- If the user did not name a chain, ask — do not guess. Discover chain IDs with `mm chains list`.

## mm transfer

### Syntax

```bash
mm transfer --to <address> --amount <amount> --chain-id <chain-id> --token <token> [--wait]
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--to` | `^0x[0-9a-fA-F]{40}$` | Recipient address |
| `--amount` | decimal `^\d+\.?\d*$`, > 0 | Human-readable amount (`0.5`, `100`). Not wei. |
| `--chain-id` | integer `^\d+$` | EVM chain ID (`1` = Ethereum, `137` = Polygon) |
| `--token` | symbol or `<address>` | Native token: symbol (`ETH`, `POL`). ERC-20: the contract address, not the symbol. |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--wait` | off | boolean flag | Block until the transfer completes (server-wallet mode only; BYOK returns immediately) |

Global flags and `--wallet-timeout` apply — see SKILL.md § Global flags. BYOK with an encrypted
mnemonic: set `MM_PASSWORD` first (references/concepts.md).

### Output

```json
{"ok": true, "data": {"pollingId": "..."}}
```
<!-- shape from CLI flag metadata; not a captured run -->

Capture: `pollingId` → use as `<polling-id>` in `mm wallet requests watch --polling-id <polling-id>`.

### Async

Without `--wait` the command returns a `pollingId` immediately. Track it via
references/wallet-requests.md and show the request's `intent` string to the user.

### Confirm before executing

Show the user ALL of: recipient, amount, token, chain. Do not run until the user approves.

### Examples

```bash
# 0.5 ETH on Ethereum mainnet, wait for completion
mm transfer --to 0x742d35Cc6634C0532925a3b844Bc454e4438f44e --amount 0.5 --chain-id 1 --token ETH --wait --toon
# 100 USDC on Polygon, by contract address
mm transfer --to 0x742d35Cc6634C0532925a3b844Bc454e4438f44e --amount 100 --chain-id 137 --token 0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359 --toon
```

### Errors

| Code | Cause | Recovery |
| --- | --- | --- |
| `ValidationError` | Malformed flag value | Re-check each value against the table above; ask the user for the full value |
| `WALLET_ERROR` | Insufficient balance or gas | Run `mm wallet balance --chain <chain-id>`; offer a swap or bridge, then retry |
| `NOT_INITIALIZED` | Project has no wallet mode | Follow workflows/onboarding.md, then retry |

Full code list: references/errors.md.
