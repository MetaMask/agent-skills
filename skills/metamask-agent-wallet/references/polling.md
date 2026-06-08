# Polling Commands

In server wallet mode, signing and transaction commands return a `pollingId` instead of an immediate result. Use these commands to track and wait for results. Both commands are server-wallet mode only.

Transfers, swaps, perps, predict orders, and predict withdraws attach a human-readable `intent` summary to their request (e.g. `Transfer 0.5 ETH to 0x...`, `Withdraw 10 pUSD to 0x...`). When listing or watching requests, surface the `intent` so the user can confirm what they are approving.

## `wallet requests list` Command

List all pending wallet requests.

### Syntax

```bash
mm wallet requests list [--sync] [--toon]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--sync` | No | Refresh pending requests before listing (defaults to true; use `--no-sync` to skip) |

### Example

```bash
mm wallet requests list
mm wallet requests list --no-sync --toon
```

## `wallet requests watch` Command

Wait for a specific wallet request to complete by its polling ID. MFA prompts are surfaced once when a job enters the `AWAITING_MFA` state.

### Syntax

```bash
mm wallet requests watch <polling-id> [--polling-id <id>] [--toon]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `<polling-id>` | Yes | Request polling ID returned by a previous command (positional) |
| `--polling-id` | No | Same as positional `<polling-id>` |

### Example

```bash
mm wallet requests watch abc-123
mm wallet requests watch --polling-id abc-123 --toon
```
