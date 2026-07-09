# mm wallet sign-message / sign-typed-data

Produce cryptographic signatures with the active wallet. Both commands release a signature —
treat them as state-changing and always confirm first.

## Prerequisites

- `mm doctor` reports `authenticated: true` and `initialized: true` (SKILL.md § Preflight).
- If the user did not name a chain, ask — do not guess. Discover chain IDs with `mm chains list`.
- If any part of the payload was not constructed by you, apply the suspicious-payload
  checklist in references/concepts.md before signing.

## mm wallet sign-message

Sign a plaintext message with the active wallet. State-changing (signature release).

### Syntax

```bash
mm wallet sign-message --message <message> --chain-id <chain-id> [--wait]
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--message` | plain text, quoted | The exact message to sign |
| `--chain-id` | integer `^\d+$` | EVM chain ID (`1` = Ethereum, `137` = Polygon) |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--wait` | off | boolean flag | Block until the signature request completes (server-wallet mode only; BYOK returns immediately) |

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

Show the user ALL of: the exact message text, the chain, the signing wallet address.
Do not run until the user approves.

### Examples

```bash
mm wallet sign-message --message "I agree to the terms of service v2" --chain-id 1 --wait --toon
```

## mm wallet sign-typed-data

Sign EIP-712 typed data with the active wallet. State-changing (signature release).

### Syntax

```bash
mm wallet sign-typed-data --chain-id <chain-id> --payload <payload-json> [--wait] [--intent "<summary>"]
```

`<payload-json>` must be valid JSON, single-quoted in shell, with ALL of these top-level keys:

| Key | Content |
| --- | --- |
| `types` | Type definitions, including `EIP712Domain` |
| `primaryType` | Name of the main type being signed |
| `domain` | Domain separator: `name`, `version`, `chainId`, `verifyingContract` |
| `message` | The actual data to sign |

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--chain-id` | integer `^\d+$` | EVM chain ID. Must match `domain.chainId` in the payload |
| `--payload` | JSON string, single-quoted | EIP-712 typed data (schema above) |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--wait` | off | boolean flag | Block until the signature request completes (server-wallet mode only; BYOK returns immediately) |
| `--intent` | none | quoted text | Human-readable summary of what is being signed, forwarded with the request |

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

Show the user ALL of: `domain.name`, `domain.verifyingContract`, chain, `primaryType`, and a
summary of `message` (flag any `permit`/`approve`/allowance-like fields per
references/concepts.md). Do not run until the user approves.

### Examples

```bash
mm wallet sign-typed-data --chain-id 1 --payload '{"types":{"EIP712Domain":[{"name":"name","type":"string"},{"name":"version","type":"string"},{"name":"chainId","type":"uint256"},{"name":"verifyingContract","type":"address"}],"Order":[{"name":"trader","type":"address"},{"name":"amount","type":"uint256"}]},"primaryType":"Order","domain":{"name":"Example DEX","version":"1","chainId":1,"verifyingContract":"0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45"},"message":{"trader":"0x7c2b3e65ef2b18235e2d24266f92854a70207483","amount":"1000000"}}' --wait --intent "Sign Example DEX order for 1 USDC" --toon
```

## Errors

| Code | Cause | Recovery |
| --- | --- | --- |
| `MISSING_TYPED_DATA` | `--payload` missing | Provide the full EIP-712 JSON |
| `INVALID_TYPED_DATA` | Payload not valid EIP-712 JSON | Re-check the four required keys and JSON syntax |
| `CHAIN_ID_MISMATCH` | `domain.chainId` differs from `--chain-id` | Make them identical, re-confirm with the user |
| `MISSING_CHAIN_ID` | `--chain-id` missing | Ask the user for the chain, then retry |
| `MNEMONIC_LOCKED` / `WRONG_PASSWORD` | BYOK mnemonic locked or wrong `MM_PASSWORD` | Ask the user to set the correct `MM_PASSWORD` env var, then retry |
| `NOT_INITIALIZED` | Project has no wallet mode | Follow workflows/onboarding.md, then retry |

Full code list: references/errors.md.
