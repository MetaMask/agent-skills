# mm predict (account & funding)

Set up, fund, and inspect the Predict (Polymarket) trading account: mode, one-time setup,
credentials, approvals, status, geoblock, balance, deposit, withdraw.

## Prerequisites

- `mm doctor` reports `authenticated: true` and `initialized: true` (SKILL.md § Preflight).
- Setup gate: `mm predict status` must show `setupComplete: true` before any trading command
  (references/predict-trade.md). If `false`, run `mm predict setup --wait` first.
- Deposits convert USDC.e held by the owner EOA on Polygon (chain 137) into pUSD in the
  Predict deposit wallet; withdrawals convert pUSD back out.
- Market/token discovery: references/predict-data.md. Orders: references/predict-trade.md.
- Async job IDs from setup/approve/deposit/withdraw are tracked with
  `mm predict watch --id <polling-id> --wait` (references/predict-trade.md).

## mm predict mode

Show or switch the Predict trading mode (local setting). Read-only when bare. Positional-only —
there is no flag form.

### Syntax

```bash
mm predict mode [mainnet|testnet]
```

Bare form shows the current mode; with an argument it switches. No command-specific flags.
Global flags apply — see SKILL.md § Global flags.

### Output

`{"ok": true, "data": {command: mode, result: {mode: mainnet}}}` <!-- shape from CLI flag metadata; not a captured run -->

### Examples

```bash
mm predict mode --toon
mm predict mode mainnet --toon
```

## mm predict setup

One-time setup: creates trading credentials, deploys the deposit wallet, sets approvals. State-changing.

### Syntax

```bash
mm predict setup [--wait]
```

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--wait` | off | boolean flag | Block until the setup job completes (prefer this) |

Global flags apply — see SKILL.md § Global flags. BYOK with an encrypted mnemonic: set
`MM_PASSWORD` first (references/concepts.md).

### Output

`{"ok": true, "data": {result: {pollingId: "..."}}}` <!-- shape from CLI flag metadata; not a captured run -->

Capture: `pollingId` → use as `<polling-id>` in `mm predict watch --id <polling-id> --wait`.

### Async

Without `--wait` a job ID is returned; track it with `mm predict watch --id <polling-id> --wait`.

### Confirm before executing

Show the user: that setup deploys a deposit wallet and grants token approvals on Polygon, and
the active Predict mode (`mm predict mode`). Do not run until the user approves.

### Examples

```bash
mm predict setup --wait --toon
```

## mm predict auth

Create or refresh Predict trading credentials (API key + CLOB signing). State-changing
(local credentials only; no on-chain effect, no confirmation needed).

### Syntax

```bash
mm predict auth [--refresh]
```

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--refresh` | off | boolean flag | Force-create or refresh trading credentials |

Global flags apply — see SKILL.md § Global flags. BYOK with an encrypted mnemonic: set
`MM_PASSWORD` first (references/concepts.md).

### Output

`{"ok": true, "data": {result: {credentials: true}}}` <!-- shape from CLI flag metadata; not a captured run -->

### Async

Completes inline; no `pollingId`.

### Confirm before executing

None required — no on-chain effect. Mention that credentials will be (re)created.

### Examples

```bash
mm predict auth --refresh --toon
```

## mm predict approve

Repair missing deposit-wallet approvals. State-changing.

### Syntax

```bash
mm predict approve [--wait]
```

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--wait` | off | boolean flag | Block until the approval job completes |

Global flags apply — see SKILL.md § Global flags. BYOK with an encrypted mnemonic: set
`MM_PASSWORD` first (references/concepts.md).

### Output

`{"ok": true, "data": {result: {pollingId: "..."}}}` <!-- shape from CLI flag metadata; not a captured run -->

Capture: `pollingId` → use as `<polling-id>` in `mm predict watch --id <polling-id> --wait`.

### Async

Without `--wait`, track the job with `mm predict watch --id <polling-id> --wait`.

### Confirm before executing

Show the user: that this grants token approvals from the Predict deposit wallet on Polygon.

### Examples

```bash
mm predict approve --wait --toon
```

## mm predict status

Probe Predict back-end reachability (Gamma + CLOB) and report account setup state. Read-only.

### Syntax

```bash
mm predict status
```

No command-specific flags. Global flags apply — see SKILL.md § Global flags.

### Output

```yaml
ok: true
data:
  command: status
  result:
    chainId: 137
    gamma: ok
    clob: ok
    account:
      ownerAddress: 0x7c2b3e65ef2b18235e2d24266f92854a70207483
      depositWalletAddress: 0xb5B5A96FD0AfdC6ba006D8a04f2F3f20a8B6f982
      deployed: false
      credentials: false
      setupComplete: false
```

Capture: `account.setupComplete` → if `false`, run `mm predict setup --wait` before trading.

### Examples

```bash
mm predict status --toon
```

## mm predict geoblock

Check whether Polymarket access is geoblocked for the current IP. Read-only. Cheaper than
letting `mm predict setup` abort with `PREDICT_GEOBLOCKED`.

### Syntax

```bash
mm predict geoblock
```

No command-specific flags. Global flags apply — see SKILL.md § Global flags.

### Output

`{"ok": true, "data": {result: {blocked: false, ip: "203.0.113.7", country: "DE", region: ""}}}` <!-- shape from CLI flag metadata; not a captured run -->

### Examples

```bash
mm predict geoblock --toon
```

## mm predict balance

Check deposit-wallet funds (pUSD), approvals, and setup status. Read-only.

### Syntax

```bash
mm predict balance [--token-id <token-id>] [--sync]
```

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--token-id` | omitted | outcome token ID string | Also report the holding of one outcome token (from `mm predict markets get`) |
| `--sync` | off | boolean flag | Refresh balances and allowances before reading |

Global flags apply — see SKILL.md § Global flags. BYOK with an encrypted mnemonic: set
`MM_PASSWORD` first (references/concepts.md).

### Output

`{"ok": true, "data": {result: {pusd: "25.00", approvals: true, setupComplete: true}}}` <!-- shape from CLI flag metadata; not a captured run -->

### Examples

```bash
mm predict balance --sync --toon
```

## mm predict deposit

Convert USDC.e from the owner EOA into pUSD in the Predict deposit wallet. State-changing.

### Syntax

```bash
mm predict deposit --amount <amount> [--wait]
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--amount` | decimal `^\d+\.?\d*$`, > 0 | pUSD amount, human-readable (`5`, `100`). Not atomic units. |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--wait` | off | boolean flag | Block until the deposit job completes |

Global flags and `--wallet-timeout` apply — see SKILL.md § Global flags. BYOK with an encrypted
mnemonic: set `MM_PASSWORD` first (references/concepts.md).

### Output

`{"ok": true, "data": {result: {pollingId: "..."}}}` <!-- shape from CLI flag metadata; not a captured run -->

Capture: `pollingId` → use as `<polling-id>` in `mm predict watch --id <polling-id> --wait`.

### Async

Without `--wait`, track the job with `mm predict watch --id <polling-id> --wait`.

### Confirm before executing

Show the user ALL of: amount, source (owner EOA USDC.e on Polygon), destination (Predict
deposit wallet, as pUSD). Do not run until the user approves.

### Examples

```bash
mm predict deposit --amount 5 --wait --toon
```

## mm predict withdraw

Withdraw pUSD from the Predict deposit wallet to the owner EOA or another address. Validates
the amount against the on-chain deposit-wallet balance before signing. State-changing.

### Syntax

```bash
mm predict withdraw --amount <amount> [--to <address>] [--wait]
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--amount` | decimal `^\d+\.?\d*$`, > 0 | pUSD amount, human-readable (`5`, `100`) |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--to` | owner EOA | `^0x[0-9a-fA-F]{40}$` | Recipient address |
| `--wait` | off | boolean flag | Block until the withdraw job completes |

Global flags apply — see SKILL.md § Global flags. BYOK with an encrypted mnemonic: set
`MM_PASSWORD` first (references/concepts.md).

### Output

`{"ok": true, "data": {result: {pollingId: "..."}}}` <!-- shape from CLI flag metadata; not a captured run -->

Capture: `pollingId` → use as `<polling-id>` in `mm predict watch --id <polling-id> --wait`.

### Async

Without `--wait`, track the job with `mm predict watch --id <polling-id> --wait`.

### Confirm before executing

Show the user ALL of: amount, recipient address (say "owner EOA" explicitly when `--to` is
omitted). Do not run until the user approves.

### Examples

```bash
mm predict withdraw --amount 10 --wait --toon
mm predict withdraw --amount 5 --to 0x742d35Cc6634C0532925a3b844Bc454e4438f44e --wait --toon
```

## Errors

| Code | Cause | Recovery |
| --- | --- | --- |
| `PREDICT_GEOBLOCKED` | IP resolves to a restricted region (checked before any wallet interaction) | Confirm with `mm predict geoblock`; Predict is unavailable from this region |
| `PREDICT_SETUP_REQUIRED` | Account command run before setup completed | Run `mm predict setup --wait`, verify with `mm predict status` |
| `UNKNOWN` (`fetch failed`) | Transient network failure to the Predict back end | Retry; check reachability with `mm predict status` |
| `WALLET_ERROR` | Insufficient USDC.e (deposit) or pUSD (withdraw) | Check `mm wallet balance --chain 137` or `mm predict balance --sync`; adjust amount |

Full code list: references/errors.md.
