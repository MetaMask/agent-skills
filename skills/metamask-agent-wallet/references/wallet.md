# Wallet Commands

Use the `wallet` commands to create, list, select, inspect wallets, and check balances.

## `wallet create` Command

Create a new wallet under the authenticated account.

### Syntax

```bash
mm-dev wallet create [--chain-namespace <namespace>] [--name <name>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--chain-namespace` | No | Wallet chain namespace: `eip155` or `solana` |
| `--name` | No | Wallet display name |

### Example

```bash
mm-dev wallet create --chain-namespace eip155
mm-dev wallet create --chain-namespace eip155 --name "Trading"
```

## `wallet list` Command

List all wallets associated with the authenticated account.

### Syntax

```bash
mm-dev wallet list [--chain-namespace <namespace>] [--toon]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--chain-namespace` | No | Filter by namespace: `eip155` or `solana` |

### Example

```bash
mm-dev wallet list
mm-dev wallet list --chain-namespace solana --toon
```

## `wallet select` Command

Switch the active wallet used for subsequent commands.

### Syntax

```bash
mm-dev wallet select [--chain-namespace <namespace>] [--id <id>] [--address <address>] [--name <name>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--chain-namespace` | No | Filter by namespace |
| `--id` | No | Wallet ID |
| `--address` | No | Wallet address |
| `--name` | No | Wallet name |

### Example

```bash
mm-dev wallet select --address 0x742d...f2bD18
mm-dev wallet select --name "Trading"
```

## `wallet show` Command

Display details for a specific wallet or the currently active wallet.

### Syntax

```bash
mm-dev wallet show [--chain-namespace <namespace>] [--id <id>] [--address <address>] [--name <name>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--chain-namespace` | No | Filter by namespace |
| `--id` | No | Wallet ID |
| `--address` | No | Wallet address |
| `--name` | No | Wallet name |

### Example

```bash
mm-dev wallet show
mm-dev wallet show --address 0x742d...f2bD18
```

## `wallet address` Command

Print the address of the currently active wallet.

### Syntax

```bash
mm-dev wallet address [--chain-namespace <namespace>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--chain-namespace` | No | Wallet chain namespace |

### Example

```bash
mm-dev wallet address
mm-dev wallet address --chain-namespace eip155
```

## `wallet balance` Command

Show native and token balances for the active wallet.

### Syntax

```bash
mm-dev wallet balance [--currency <code>] [--chain <chains>] [--token <token>] [--address <address>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--currency` | No | Fiat currency code |
| `--chain` | No | Comma-separated chain filters (chain id, CAIP-2 id, or chain key) |
| `--token` | No | Token filter (symbol, token address, or CAIP-19 asset id) |
| `--address` | No | Wallet address |

### Example

```bash
mm-dev wallet balance
mm-dev wallet balance --chain 8453
mm-dev wallet balance --token USDC
mm-dev wallet balance --currency eur
```
