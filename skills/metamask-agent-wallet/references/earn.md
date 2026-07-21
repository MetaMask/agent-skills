# Earn Commands

Use the `earn` commands to browse DeFi yield vaults, view positions, supply tokens, and withdraw. Powered by LiFi's earn API.

## `earn markets` Command

List available earn vaults with APY and TVL data. Does not require authentication.

### Syntax

```bash
mm earn markets [--chain <chain-id>] [--protocol <name>] [--min-tvl <usd>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--chain` | No | EVM chain ID to filter results (e.g. 1 for Ethereum, 8453 for Base) |
| `--protocol` | No | Filter by protocol name (e.g. aave, compound, morpho) |
| `--min-tvl` | No | Minimum TVL in USD. Must be a positive number |

### Example

```bash
mm earn markets
mm earn markets --chain 8453
mm earn markets --chain 1 --protocol aave --min-tvl 100000
```

### Output

Each vault includes: address, chainId, name, protocol, underlying tokens, APY (base/reward/total), 7-day and 30-day APY, TVL in USD, and whether it supports deposits (`isTransactional`) and withdrawals (`isRedeemable`).

## `earn positions` Command

List current earn positions (deposited balances) for a wallet. Does not require authentication.

### Syntax

```bash
mm earn positions [--chain <chain-id>] [--address <address>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--chain` | No | EVM chain ID to filter positions |
| `--address` | No | Account address. Defaults to the currently selected wallet |

### Example

```bash
mm earn positions
mm earn positions --chain 8453
mm earn positions --address 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18
```

### Output

Each position includes: chainId, vault address, protocol name, asset (address/symbol/decimals/name), balance in USD, and balance in native token units.

## `earn supply` Command

Supply tokens to an earn vault to earn yield. Requires authentication. Handles ERC-20 approval automatically. Supports cross-chain deposits.

### Syntax

```bash
mm earn supply --token <symbol|address> --amount <amount> --chain <chain-id> [--vault <address>] [--protocol <name>] [--from-chain <chain-id>] [--from-token <symbol|address>] [--password <password>] [--wallet-timeout <seconds>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--token` | Yes (unless `--vault`) | Underlying token symbol or contract address (e.g. USDC) |
| `--amount` | Yes | Human-readable amount to supply (e.g. 100). Must be a positive number |
| `--chain` | Yes | Destination EVM chain ID where the vault lives |
| `--vault` | No | Vault contract address. If omitted, auto-selects the best vault for the token |
| `--protocol` | No | Restrict vault auto-selection to a specific protocol (e.g. aave, compound) |
| `--from-chain` | No | Source chain ID for cross-chain deposits |
| `--from-token` | No | Source token symbol or address for cross-chain deposits. Required when `--from-chain` differs from `--chain` |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |
| `--wallet-timeout` | No | Seconds to wait per wallet job (MFA/signing), max 600; overrides config `walletTimeoutSeconds` |

### Validation Rules

- Either `--token` or `--vault` must be provided.
- When `--from-chain` differs from `--chain`, `--from-token` is required.

### Example

```bash
mm earn supply --token USDC --amount 100 --chain 8453
mm earn supply --token USDC --amount 100 --chain 8453 --protocol aave
mm earn supply --vault 0xabc...def --amount 50 --chain 1
mm earn supply --token USDC --amount 100 --chain 8453 --from-chain 1 --from-token USDC
```

## `earn withdraw` Command

Withdraw tokens from an earn vault. Requires authentication. Handles LP token approval automatically.

### Syntax

```bash
mm earn withdraw --token <symbol|address> --amount <amount> --chain <chain-id> [--vault <address>] [--protocol <name>] [--all] [--password <password>] [--wallet-timeout <seconds>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--token` | Yes (unless `--vault`) | Underlying token symbol or contract address |
| `--amount` | Yes (unless `--all`) | Human-readable amount to withdraw. Must be a positive number |
| `--chain` | Yes | EVM chain ID of the vault |
| `--vault` | No | Vault contract address. If omitted, auto-selects by token |
| `--protocol` | No | Restrict vault auto-selection to a specific protocol |
| `--all` | No | Withdraw the full balance. Mutually exclusive with `--amount` |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |
| `--wallet-timeout` | No | Seconds to wait per wallet job (MFA/signing), max 600; overrides config `walletTimeoutSeconds` |

### Validation Rules

- Either `--token` or `--vault` must be provided.
- Either `--amount` or `--all` must be provided.
- The vault must be redeemable (`isRedeemable: true`). If not, the CLI returns `NOT_REDEEMABLE`.

### Example

```bash
mm earn withdraw --token USDC --amount 50 --chain 8453
mm earn withdraw --token USDC --all --chain 8453
mm earn withdraw --vault 0xabc...def --all --chain 1
```

## Notes

- Use `mm earn markets` to discover available vaults before supplying.
- Use `mm earn positions` to check current deposits before withdrawing.
- If `--vault` is omitted, the CLI auto-selects the best vault for the token on the specified chain. Use `--protocol` to narrow the selection.
- Cross-chain supply is supported: set `--from-chain` and `--from-token` to deposit from a different chain. The CLI routes through LiFi and polls until the cross-chain transaction completes (timeout: 10 minutes).
- The CLI handles ERC-20 approvals automatically for both supply and withdraw operations.
