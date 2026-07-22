# Wallet Commands

Use the `wallet` commands to create, list, select, inspect wallets, and check balances.

## `wallet create` Command

Create a new wallet under the authenticated account.

### Syntax

```bash
mm wallet create [--chain-namespace <namespace>] [--name <name>] [--trading-mode <mode>] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--chain-namespace` | No | Wallet chain namespace: `evm` (EIP-155) (allowed: `evm`) |
| `--name` | No | Display name for the wallet |
| `--trading-mode` | No | `guard` enforces outflow/whitelist policies and blocks malicious transactions. `beast` skips policy checks but still blocks malicious transactions (allowed: `guard`, `beast`) |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm wallet create --chain-namespace evm
mm wallet create --chain-namespace evm --name "Trading"
mm wallet create --chain-namespace evm --name "Fast Trading" --trading-mode beast
```

## `wallet list` Command

List all wallets associated with the authenticated account.

### Syntax

```bash
mm wallet list [--chain-namespace <namespace>] [--toon]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--chain-namespace` | No | Filter by namespace: `evm` (EIP-155) (allowed: `evm`) |

### Example

```bash
mm wallet list
mm wallet list --chain-namespace evm --toon
```

## `wallet select` Command

Switch the active wallet used for subsequent commands.

### Syntax

```bash
mm wallet select [--chain-namespace <namespace>] [--id <id>] [--address <address>] [--name <name>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--chain-namespace` | No | Filter by namespace: `evm` (EIP-155) (allowed: `evm`) |
| `--id` | No | Wallet ID |
| `--address` | No | Wallet address (0x-prefixed hex) |
| `--name` | No | Wallet display name |

### Example

```bash
mm wallet select --address 0x742d...f2bD18
mm wallet select --name "Trading"
```

## `wallet show` Command

Display details for a specific wallet or the currently active wallet.

### Syntax

```bash
mm wallet show [--chain-namespace <namespace>] [--id <id>] [--address <address>] [--name <name>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--chain-namespace` | No | Filter by namespace: `evm` (EIP-155) (allowed: `evm`) |
| `--id` | No | Wallet ID |
| `--address` | No | Wallet address (0x-prefixed hex) |
| `--name` | No | Wallet display name |

### Example

```bash
mm wallet show
mm wallet show --address 0x742d...f2bD18
```

## `wallet address` Command

Print the address of the currently active wallet.

### Syntax

```bash
mm wallet address [--chain-namespace <namespace>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--chain-namespace` | No | Wallet chain namespace: `evm` (EIP-155) (allowed: `evm`) |

### Example

```bash
mm wallet address
mm wallet address --chain-namespace evm
```

## `wallet add-fund` Command

Show a QR code and address to fund the currently active wallet. In interactive mode (TTY or REPL), renders an ASCII QR code plus the address. In headless mode (`--json`, piped stdout), outputs the address only.

### Syntax

```bash
mm wallet add-fund [--chain-namespace <namespace>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--chain-namespace` | No | Wallet chain namespace: `evm` (EIP-155) (allowed: `evm`) |

### Example

```bash
mm wallet add-fund
mm wallet add-fund --toon
```

## `wallet trading-mode get` Command

Show the current trading mode and active wallet address for the selected wallet.

### Syntax

```bash
mm wallet trading-mode get
```

### Example

```bash
mm wallet trading-mode get
```

## `wallet trading-mode set` Command

Set the trading mode for the active wallet. Broadening changes (guard → beast) require MFA approval; tightening changes (beast → guard) apply immediately. Returns `confirmed` when applied, or `pending_approval` while awaiting MFA.

### Syntax

```bash
mm wallet trading-mode set <guard|beast> [--wait] [--wallet-timeout <seconds>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `<mode>` | Yes | `guard` enforces outflow/whitelist policies and blocks malicious transactions. `beast` skips policy checks but still blocks malicious transactions |
| `--wait` | No | Block until MFA approval completes. Use `--no-wait` to return immediately with the request ID |
| `--wallet-timeout` | No | Seconds to wait per wallet job (MFA/signing), max 600; overrides config `walletTimeoutSeconds` |

### Example

```bash
mm wallet trading-mode set guard
mm wallet trading-mode set beast --wait
mm wallet trading-mode set beast --wallet-timeout 300
```

## `wallet policy get` Command

Show the policy for the active wallet.

### Syntax

```bash
mm wallet policy get
```

### Supported Flags

This command does not support additional flags beyond output format options.

### Example

```bash
mm wallet policy get
mm wallet policy get --toon
```

## `wallet policy set` Command

Set the policy for the active wallet. Broadening policy changes (e.g. increasing outflow limits) require MFA approval; non-broadening changes (e.g. tightening limits) apply immediately. Returns `confirmed` when applied immediately, or `pending_approval` when MFA is required.

### Syntax

```bash
mm wallet policy set --policy <yaml> [--wait] [--wallet-timeout <seconds>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--policy` | Yes | Policy string to apply |
| `--wait` | No | Block until MFA approval completes. Use `--no-wait` to return immediately with the request ID |
| `--wallet-timeout` | No | Seconds to wait per wallet job (MFA/signing), max 600; overrides config `walletTimeoutSeconds` |

### Example

```bash
mm wallet policy set --policy "maxDailyOutflow: 1000"
mm wallet policy set --policy "maxDailyOutflow: 5000" --wait
```

## `wallet policy template` Command

Show the project policy template.

### Syntax

```bash
mm wallet policy template
```

### Supported Flags

This command does not support additional flags beyond output format options.

### Example

```bash
mm wallet policy template
mm wallet policy template --toon
```

## `wallet balance` Command

Show native and token balances for the active wallet.

### Syntax

```bash
mm wallet balance [--currency <code>] [--chain <chains>] [--token <token>] [--address <address>] [--testnet] [--testnet-chain-id <ids>] [--token-contracts <addresses>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--currency` | No | Fiat currency code for price conversion (e.g. usd, eur) |
| `--chain` | No | Comma-separated chain filters (e.g. `1,137` or `eip155:1`). Run `mm chains list` to see options |
| `--token` | No | Filter by token symbol, contract address, or CAIP-19 asset ID (e.g. USDC, 0xa0b8...) |
| `--address` | No | Wallet address (0x-prefixed hex) |
| `--testnet` | No | Read balances via RPC on Arbitrum Sepolia, Amoy, and Sepolia testnets |
| `--testnet-chain-id` | No | Comma-separated EVM testnet chain IDs for on-chain RPC balance reads (e.g. `421614,80002`) |
| `--token-contracts` | No | Comma-separated ERC-20 contract addresses for testnet RPC chains (0x-prefixed hex). Use with `--testnet-chain-id` to read specific token balances on testnets |

### Example

```bash
mm wallet balance
mm wallet balance --chain 8453
mm wallet balance --token USDC
mm wallet balance --currency eur
mm wallet balance --testnet
mm wallet balance --testnet-chain-id 421614 --token-contracts 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48
```
