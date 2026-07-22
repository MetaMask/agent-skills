# Earn Supply Workflow

Use this workflow when the user wants to deposit tokens into a DeFi earn vault to earn yield.

Reference command syntax in `references/earn.md`.

## Flow

1. Discover vaults.
2. Confirm with the user.
3. Supply and track status.

## Discover Vaults

Find available vaults for the token and chain:

```bash
mm earn markets --chain 8453 --protocol aave
```

Show the user relevant vaults with their APY, TVL, and protocol. Let the user pick if multiple vaults are available.

## Check Balance

Verify the user has enough of the token to supply:

```bash
mm wallet balance --chain 8453 --token USDC
```

## Supply

Same-chain:

```bash
mm earn supply --token USDC --amount 100 --chain 8453
```

With a specific vault or protocol:

```bash
mm earn supply --token USDC --amount 100 --chain 8453 --protocol aave
mm earn supply --vault 0xabc...def --amount 100 --chain 8453
```

Cross-chain (supply from a different chain):

```bash
mm earn supply --token USDC --amount 100 --chain 8453 --from-chain 1 --from-token USDC
```

## Confirm

Before executing, confirm with the user: token, amount, chain, vault/protocol, and APY. For cross-chain supply, also confirm the source chain and source token.

## Edge cases

- `VAULT_NOT_FOUND`: no matching vault for the token/chain/protocol. Run `mm earn markets` to check available options.
- `UNSUPPORTED_CHAIN`: chain not supported by earn. Run `mm chains list` to check.
- `INSUFFICIENT_FUNDS`: wallet lacks the token balance. Fund the wallet first.
- `EXECUTE_FAILED`: transaction reverted or cross-chain timeout. Retry or check the transaction on the block explorer.
- `QUOTE_FAILED`: LiFi returned no executable transaction. Try a different vault or amount.
- Cross-chain supply: when `--from-chain` differs from `--chain`, `--from-token` is required. The CLI polls until the cross-chain transaction completes (timeout: 10 minutes).
