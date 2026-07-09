# mm wallet send-transaction

Send a raw EVM transaction from the active wallet. State-changing.

## Prerequisites

- `mm doctor` reports `authenticated: true` and `initialized: true` (SKILL.md § Preflight).
- If the user did not name a chain, ask — do not guess. Discover chain IDs with `mm chains list`.
- If the calldata was not constructed by you, decode it FIRST with
  `mm decode --payload <calldata>` (references/decode.md) and confirm the decoded intent with
  the user before sending. Apply the suspicious-payload checklist in references/concepts.md.
- For simple native/ERC-20 transfers prefer `mm transfer` (references/transfer.md).

## mm wallet send-transaction

### Syntax

```bash
mm wallet send-transaction --chain-id <chain-id> --payload <payload-json> [--wait] [--intent "<summary>"]
```

`<payload-json>` is a JSON string, single-quoted in shell:

```json
{
  "to": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "value": "0xde0b6b3a7640000",
  "data": "0x"
}
```

| Key | Required | Format | Description |
| --- | --- | --- | --- |
| `to` | Yes | `^0x[0-9a-fA-F]{40}$` | Destination address |
| `value` | No | `0x`-prefixed hex wei, NOT decimal | Native amount. Convert decimals with `python3 "$SKILL_DIR/scripts/amount_to_hex.py" <amount> 18` |
| `data` | No | `^0x[0-9a-fA-F]*$` | Calldata (`0x` for plain sends) |

Optional payload keys: `gas`, `nonce`, `maxFeePerGas`, `maxPriorityFeePerGas`.

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--chain-id` | integer `^\d+$` | EVM chain ID (`1` = Ethereum, `137` = Polygon) |
| `--payload` | JSON string, single-quoted | Transaction payload (schema above) |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--wait` | off | boolean flag | Block until the transaction completes (server-wallet mode only; BYOK returns immediately) |
| `--intent` | none | quoted text | Human-readable summary of what the transaction does, forwarded with the request |

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

Show the user ALL of: `to` address, native `value` in human units, decoded meaning of `data`
(via `mm decode` when non-empty), chain, and the `--intent` text. Do not run until the user
approves.

### Examples

```bash
# Send 1 ETH on Ethereum mainnet
mm wallet send-transaction --chain-id 1 --payload '{"to":"0x742d35Cc6634C0532925a3b844Bc454e4438f44e","value":"0xde0b6b3a7640000","data":"0x"}' --intent "Send 1 ETH to 0x742d35Cc6634C0532925a3b844Bc454e4438f44e" --wait --toon
# ERC-20 transfer of 1 USDC on Ethereum via calldata (decode-confirmed first)
mm wallet send-transaction --chain-id 1 --payload '{"to":"0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48","value":"0x0","data":"0xa9059cbb000000000000000000000000742d35cc6634c0532925a3b844bc454e4438f44e00000000000000000000000000000000000000000000000000000000000f4240"}' --intent "Transfer 1 USDC to 0x742d35Cc6634C0532925a3b844Bc454e4438f44e" --toon
```

## Errors

| Code | Cause | Recovery |
| --- | --- | --- |
| `MISSING_TRANSACTION_PAYLOAD` | `--payload` missing | Provide the JSON payload |
| `INVALID_TRANSACTION_PAYLOAD` | Payload not valid JSON or missing `to` | Re-check the schema above; `value` must be hex, not decimal |
| `INVALID_TO` | `to` is not a valid address | Ask the user for the full 40-hex address |
| `INVALID_QUANTITY` | `value` not `0x`-prefixed hex | Convert with `scripts/amount_to_hex.py` |
| `WALLET_ERROR` | Insufficient balance/gas or on-chain revert | Run `mm wallet balance --chain <chain-id>`; inspect with `mm decode`; retry after funding |
| `NOT_INITIALIZED` | Project has no wallet mode | Follow workflows/onboarding.md, then retry |

Full code list: references/errors.md.
