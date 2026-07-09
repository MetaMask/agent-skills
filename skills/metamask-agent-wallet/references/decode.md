# mm decode

Turn raw EVM calldata into a human-readable intent before signing or sending. Run this on any
calldata you did not construct yourself (SKILL.md § Safety invariants).

## Prerequisites

- `mm doctor` reports `authenticated: true` and `initialized: true` (SKILL.md § Preflight).

## mm decode

Decode hex calldata into function name, parameters, and a plain-language `intent`. Read-only.

### Syntax

```bash
mm decode --payload <calldata>
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--payload` | `^0x[0-9a-fA-F]+$` | Hex-encoded EVM calldata to decode |

### Optional flags

None beyond global flags.

Global flags apply — see SKILL.md § Global flags.

### Output

```
ok: true
data:
  functionName: transfer
  params[2]{name,type,value}:
    param0,address,0x742d35Cc6634C0532925a3b844Bc454e4438f44e
    param1,uint256,"1000000"
  intent: "Call transfer(param0: 0x742d35Cc6634C0532925a3b844Bc454e4438f44e, param1: 1000000)"
```

Capture: `intent` → show to the user verbatim when confirming a transaction or signature.

### Examples

```bash
# ERC-20 transfer(to, amount) calldata — 1 USDC (6 decimals) to 0x742d…
mm decode --payload 0xa9059cbb000000000000000000000000742d35cc6634c0532925a3b844bc454e4438f44e00000000000000000000000000000000000000000000000000000000000f4240 --toon
```

## Errors

| Code | Cause | Recovery |
| --- | --- | --- |
| `INVALID_DATA` | Payload is not valid hex calldata | Re-check the `0x` prefix and hex characters |
| `NOT_INITIALIZED` | Project has no wallet mode | Follow workflows/onboarding.md, then retry |

If the selector is not recognized, `intent` falls back to `Call unknown function`. Treat
unrecognized calldata as higher risk and warn the user before proceeding.

Full code list: references/errors.md.
