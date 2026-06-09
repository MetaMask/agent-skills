# Aave V3 withdraw workflow

Use this workflow to withdraw supplied assets from Aave V3.

## Flow

1. Resolve chain, asset address, and pool address.
2. Check positions and health factor.
3. Query the Aave API for the withdraw transaction.
4. Execute withdrawal.

## Resolve chain and addresses

If the user doesn't specify a chain, ask. Look up the pool address:

| Chain | Chain ID | Pool address |
| --- | --- | --- |
| Ethereum | 1 | `0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2` |
| Polygon | 137 | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` |
| Arbitrum | 42161 | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` |
| Optimism | 10 | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` |
| Avalanche | 43114 | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` |
| Base | 8453 | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` |

## Check positions

Check the user's current positions using `aave-positions.md`. Confirm the asset and available balance.

Before a full withdrawal, query `userBorrows` and verify there's no outstanding debt. A full collateral withdrawal fails if any debt exists, even tiny "dust" amounts. The transaction reverts with error `0x6679996d`. Follow `aave-repay.md` to clear all debt first.

For a partial withdrawal with outstanding borrows, preview the health factor impact:

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "{ healthFactorPreview(request: { action: { withdraw: { market: \"<POOL_ADDRESS>\", sender: \"<WALLET_ADDRESS>\", chainId: <CHAIN_ID>, amount: { erc20: { currency: \"<ASSET_ADDRESS>\", value: { exact: \"<AMOUNT>\" } } } } } }) { before after } }"
  }'
```

If the projected health factor (`after`) drops below 1.5, warn about liquidation risk. If it drops below 1.0, stop and tell the user to repay debt first.

## Query withdraw transaction

Get the wallet address and query the Aave V3 GraphQL API:

```bash
mm wallet address
```

For a specific amount:

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "{ withdraw(request: { market: \"<POOL_ADDRESS>\", amount: { erc20: { currency: \"<ASSET_ADDRESS>\", value: { exact: \"<AMOUNT>\" } } }, sender: \"<WALLET_ADDRESS>\", chainId: <CHAIN_ID> }) { __typename ... on TransactionRequest { to from data value chainId } ... on ApprovalRequired { approval { to from data value chainId } originalTransaction { to from data value chainId } } ... on InsufficientBalanceError { required { value decimals } available { value decimals } } } }"
  }'
```

To withdraw the full balance, use `{ max: true }` instead of `{ exact: \"<AMOUNT>\" }` in the value field.

## Execute withdrawal

Confirm the asset, amount (or "full balance"), destination, and chain with the user. The `value` field must be `0x`-prefixed hex (typically `"0x0"` for ERC-20 withdrawals).

```bash
mm wallet send-transaction --chain-id <CHAIN_ID> --payload '{"to":"<TO>","value":"0x0","data":"<DATA>"}' --wait --intent "Withdraw <AMOUNT> <SYMBOL> from Aave V3 on <CHAIN_NAME>"
```

If the response is `ApprovalRequired`, send the approval transaction first, then the withdrawal transaction (same pattern as `aave-supply.md`).

## Notes

- After the transaction confirms, use `aave-positions.md` to verify the updated position.
- Add a `recipient` field to the request to withdraw to a different address than the sender.
