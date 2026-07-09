# mm wallet

Create, list, select, and inspect wallets; check balances; manage trading mode and policy.

## Prerequisites

- `mm doctor` reports `authenticated: true` and `initialized: true` (SKILL.md § Preflight).
- Trading-mode and policy commands apply to the active server wallet (server-wallet mode only).
- `--chain-namespace` accepts only the literal value `evm`.
- Wallet selector flags (used by select/show): `--address <address>` (preferred), `--id <wallet-id>`, `--name <name>`, `--chain-namespace evm`. Pass exactly one selector.

## mm wallet create

Create a new wallet under the authenticated account. State-changing. Synchronous — no
`pollingId` is created.

### Syntax

```bash
mm wallet create --chain-namespace evm --name <name> --trading-mode <trading-mode>
```

### Required flags

None — but always pass flags explicitly in scripts (a TTY may otherwise prompt).

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--chain-namespace` | `evm` | literal `evm` | Wallet chain namespace (EIP-155) |
| `--name` | auto | string | Display name for the wallet |
| `--trading-mode` | `guard` | `guard` or `beast` | Server wallets only. `guard` enforces outflow/whitelist policies and blocks malicious transactions; `beast` skips policy checks but still blocks malicious transactions |

Global flags apply — see SKILL.md § Global flags. BYOK with an encrypted mnemonic: set
`MM_PASSWORD` first (references/concepts.md). BYOK with an
encrypted mnemonic: set `MM_PASSWORD` first (references/concepts.md).

### Confirm before executing

Only if `--trading-mode beast`: warn that policy checks will be skipped for this wallet and
wait for approval. Otherwise no confirmation needed (wallet management).

### Examples

```bash
mm wallet create --chain-namespace evm --name "Trading" --trading-mode guard --toon
mm wallet create --chain-namespace evm --name "Fast Trading" --trading-mode beast --toon
```

## mm wallet list

List all wallets for the authenticated account. Read-only.
Optional flags: `--chain-namespace evm` (namespace filter; default all).
Global flags apply — see SKILL.md § Global flags.

### Syntax

```bash
mm wallet list --toon
```

### Output

```
ok: true
data:
  mode: server
  chainNamespace: null
  wallets[1]{walletId,address,name,chainNamespace,tradingMode}:
    null,0x7c2b3e65ef2b18235e2d24266f92854a70207483,Server EVM Wallet 1,evm,beast
```

Capture: `address` → use as `<address>` in `mm wallet select --address <address>`.

## mm wallet select

Switch the active wallet for subsequent commands. State-changing (local session only;
synchronous, no `pollingId`, no user confirmation needed — state the new active address after).
Optional flags: one selector from Prerequisites. Global flags apply — see SKILL.md § Global flags.

### Syntax

```bash
mm wallet select --address <address>
```

### Examples

```bash
mm wallet select --address 0x7c2b3e65ef2b18235e2d24266f92854a70207483 --toon
```

## mm wallet show

Show details for a specific wallet, or the active wallet when no selector is passed. Read-only.
Optional flags: one selector from Prerequisites. Global flags apply — see SKILL.md § Global flags.

### Syntax

```bash
mm wallet show [--address <address>]
```

### Examples

```bash
mm wallet show --toon
```

## mm wallet address

Print the active wallet address. Read-only.
Optional flags: `--chain-namespace evm`. Global flags apply — see SKILL.md § Global flags.

### Syntax

```bash
mm wallet address --toon
```

## mm wallet balance

Show native and token balances for the active wallet. Read-only.

### Syntax

```bash
mm wallet balance [--chain <chain-id>] [--token <token>] [--currency <currency>]
```

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--chain` | all chains | comma-separated `<chain-id>` or `<caip2>` (`1,137` or `eip155:1`) | Chain filter; discover with `mm chains list` |
| `--token` | all tokens | symbol, `<address>`, or `<caip19>` | Token filter (`USDC`, contract address, or CAIP-19 ID) |
| `--currency` | `usd` | fiat code (`usd`, `eur`) | Fiat currency for price conversion |
| `--address` | active wallet | `^0x[0-9a-fA-F]{40}$` | Read balances for a different wallet address |
| `--testnet` | off | boolean flag | Read balances via RPC on Arbitrum Sepolia, Amoy, and Sepolia |
| `--testnet-chain-id` | — | comma-separated `<chain-id>` (`421614,80002`) | EVM testnet chain IDs for on-chain RPC balance reads |
| `--token-contracts` | — | comma-separated `<address>` | ERC-20 contracts to read on testnet RPC chains; use with `--testnet-chain-id` |

Global flags apply — see SKILL.md § Global flags.

### Output

```
ok: true
data:
  currency: usd
  totalValue: "0.28095449727443748075"
  chains[2]:
    - chain: "eip155:1"
      name: Ethereum
      totalValue: "0.27363681086398687225"
      tokens[1]{token,amount,usdValue,assetId,name,type}:
        ETH,"0.000157104527552167","0.27363681086398687225","eip155:1/slip44:60",Ether,native
```

### Examples

```bash
mm wallet balance --toon
mm wallet balance --chain 8453 --token USDC --toon
mm wallet balance --testnet-chain-id 421614 --token-contracts 0xaf88d065e77c8cC2239327C5EDb3A432268e5831 --toon
```

## mm wallet add-fund

Show a QR code and address to fund the active wallet. Read-only. TTY: ASCII QR plus address;
headless (`--json`/piped): address only.
Optional flags: `--chain-namespace evm`. Global flags apply — see SKILL.md § Global flags.

### Syntax

```bash
mm wallet add-fund --toon
```

## mm wallet trading-mode get

Show the trading mode of the active server wallet. Read-only. Takes NO flags beyond global
flags — the CLI's usage string for this command is wrong; never add `--chain-namespace` or
`--address` (rejected as nonexistent). Global flags apply — see SKILL.md § Global flags.

### Syntax

```bash
mm wallet trading-mode get
```

### Output

```
ok: true
data:
  mode: beast
  address: 0x7c2b3e65ef2b18235e2d24266f92854a70207483
```

## mm wallet trading-mode set

Set the trading mode of the active server wallet. State-changing (synchronous, no `pollingId`).
The mode is a POSITIONAL argument — no flag form exists, and `--chain-namespace`/`--address`
are rejected. Global flags apply — see SKILL.md § Global flags.

### Syntax

```bash
mm wallet trading-mode set <trading-mode>
```

`<trading-mode>` is `guard` or `beast` (definitions: references/concepts.md § Trading modes).

### Confirm before executing

Show the user: current mode (from `mm wallet trading-mode get`), requested mode. For `beast`,
warn that policy checks will be skipped. Do not run until the user approves.

### Examples

```bash
mm wallet trading-mode set guard --toon
mm wallet trading-mode set beast --toon
```

## mm wallet policy get

Show the policy YAML for the active server wallet. Read-only. Takes NO flags beyond global
flags (its usage string is wrong; never add `--chain-namespace` or `--address`).
Global flags apply — see SKILL.md § Global flags.

### Syntax

```bash
mm wallet policy get
```

### Output

```
ok: true
data:
  policy: "# Mimir Wallet Policy\nschema_version: 1\nwallet_address: \"0x7c2b3e65ef2b18235e2d24266f92854a70207483\"\n\naddresses:\n  allowlist: []\n  blocklist: []\n\nevm:\n  allowed_chains:\n    - 1\n    - 8453\n  outflow_limits_usd:\n    rolling_24h: 0\n"
  address: 0x7c2b3e65ef2b18235e2d24266f92854a70207483
```

Capture: `policy` → edit and reuse as `<policy-yaml>` in `mm wallet policy set --policy <policy-yaml>`.

## mm wallet policy set

Set the policy YAML for the active server wallet. State-changing (synchronous, no `pollingId`).

### Syntax

```bash
mm wallet policy set --policy <policy-yaml>
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--policy` | YAML string, single-quoted in shell | Full policy YAML to apply. Start from `mm wallet policy get` or `mm wallet policy template`, never from scratch |

Global flags apply — see SKILL.md § Global flags.

### Confirm before executing

Show the user the full policy YAML being applied and a summary of what changed versus the
current policy. Do not run until the user approves.

### Examples

```bash
mm wallet policy set --policy 'schema_version: 1
evm:
  allowed_chains:
    - 1
    - 8453
  outflow_limits_usd:
    rolling_24h: 1000' --toon
```

## mm wallet policy template

Show the project policy template YAML. Read-only. No flags beyond global flags.
Global flags apply — see SKILL.md § Global flags.

### Syntax

```bash
mm wallet policy template --toon
```

## Errors

| Code | Cause | Recovery |
| --- | --- | --- |
| `WALLET_NOT_FOUND` | Selector matched no wallet | Run `mm wallet list` and retry with an exact `--address` |
| `INVALID_TRADING_MODE` | Mode not `guard` or `beast` | Retry with exactly `guard` or `beast` |
| `ALREADY_SET_TRADING_MODE` | Requested mode already active | Nothing to do; report the current mode |
| `UNSUPPORTED_NAMESPACE` | `--chain-namespace` value not `evm` | Use `evm` |
| `NOT_INITIALIZED` | Project has no wallet mode | Follow workflows/onboarding.md, then retry |
| `NO_TTY` | Interactive prompt in headless mode | Pass all flags explicitly |

Full code list: references/errors.md.
