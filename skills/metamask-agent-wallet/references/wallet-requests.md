# mm wallet requests

Track asynchronous wallet jobs by `pollingId`. In server-wallet mode, signing and transaction
commands return a `pollingId` instead of an immediate result (references/concepts.md § Async
job model). Both commands are server-wallet mode only.

## Prerequisites

- `mm doctor` reports `authenticated: true` and `initialized: true` (SKILL.md § Preflight).
- Requests carry a human-readable `intent` string (e.g. `Transfer 0.5 ETH to 0x742d35Cc6634C0532925a3b844Bc454e4438f44e`).
  Always surface the `intent` so the user can see what they are approving.

## mm wallet requests list

List all pending wallet requests. Read-only.

### Syntax

```bash
mm wallet requests list [--no-sync]
```

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--sync` | on | boolean flag | Refetch live status for non-terminal entries; pass `--no-sync` to skip the refresh |

Global flags apply — see SKILL.md § Global flags.

### Output

```
ok: true
data:
  requests: []
```

When requests are pending, each entry includes `pollingId`, `status`, and `intent`.
Capture: `pollingId` → use as `<polling-id>` in `mm wallet requests watch --polling-id <polling-id>`.

### Examples

```bash
mm wallet requests list --toon
mm wallet requests list --no-sync --toon
```

## mm wallet requests watch

Wait for a specific wallet request to complete. Read-only (it only observes the job). MFA
prompts are surfaced once when a job enters the `AWAITING_MFA` state.

### Syntax

```bash
mm wallet requests watch --polling-id <polling-id>
```

There is no positional form — `--polling-id` is required.

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--polling-id` | string from a prior command's output | Polling ID to wait on; list pending IDs with `mm wallet requests list` |

### Optional flags

None beyond global flags.

Global flags and `--wallet-timeout` apply — see SKILL.md § Global flags.

### Output

```json
{"ok": true, "data": {"pollingId": "...", "status": "COMPLETED", "intent": "Transfer 0.5 ETH to 0x742d35Cc6634C0532925a3b844Bc454e4438f44e"}}
```
<!-- shape from CLI flag metadata; not a captured run -->

### Examples

```bash
mm wallet requests watch --polling-id 7f3c2a9e-1b4d-4e8a-9c6f-2d5b8a1e4c7f --toon
mm wallet requests watch --polling-id 7f3c2a9e-1b4d-4e8a-9c6f-2d5b8a1e4c7f --wallet-timeout 300 --toon
```

## Errors

| Code | Cause | Recovery |
| --- | --- | --- |
| `MISSING_ID` | `--polling-id` missing | Run `mm wallet requests list`, pick the ID, retry |
| `MISSING_FLAG` | Required flag omitted in headless mode | Pass `--polling-id` explicitly |
| `NOT_INITIALIZED` | Project has no wallet mode | Follow workflows/onboarding.md, then retry |

Full code list: references/errors.md.
