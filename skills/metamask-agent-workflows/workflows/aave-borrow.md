# Aave V3 borrow workflow

Use this workflow to borrow assets from Aave V3 against supplied collateral.

## Flow

1. Resolve chain, asset address, and pool address.
2. Check collateral and borrow capacity.
3. Preview health factor impact.
4. Query the Aave API for the borrow transaction and execute.

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

## Check collateral

Before borrowing, check the user's positions using `aave-positions.md`. Verify the following.

1. The user has supplied collateral. If not, follow `aave-supply.md` to supply assets first.
2. Collateral is enabled on at least one supplied asset (`isCollateral` is `true`). If not, follow `aave-collateral.md` to enable it.
3. Available borrow capacity covers the requested amount.

Query available markets to check the target asset's borrow APY and whether `borrowCapReached` is `true`. See `aave-markets.md`.

## Preview health factor

Preview the health factor impact before borrowing:

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "{ healthFactorPreview(request: { action: { borrow: { market: \"<POOL_ADDRESS>\", sender: \"<WALLET_ADDRESS>\", chainId: <CHAIN_ID>, amount: { erc20: { currency: \"<ASSET_ADDRESS>\", value: \"<AMOUNT>\" } } } } }) { before after } }"
  }'
```

Show the health factor before and after. If the projected health factor (`after`) drops below 1.5, warn about liquidation risk. If it drops below 1.0, stop and tell the user to reduce the borrow amount or repay existing debt.

## Query borrow transaction

Get the wallet address and query the Aave V3 GraphQL API. Don't include `onBehalfOf` when borrowing for the user's own account. It triggers a credit delegation requirement even for self-borrows.

```bash
mm wallet address
```

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "{ borrow(request: { market: \"<POOL_ADDRESS>\", amount: { erc20: { currency: \"<ASSET_ADDRESS>\", value: \"<AMOUNT>\" } }, sender: \"<WALLET_ADDRESS>\", chainId: <CHAIN_ID> }) { __typename ... on TransactionRequest { to from data value chainId } ... on ApprovalRequired { approval { to from data value chainId } originalTransaction { to from data value chainId } } ... on InsufficientBalanceError { required { value decimals } available { value decimals } } } }"
  }'
```

The `value` in the amount is a human-readable decimal string (e.g., `"2"`, `"100"`). The API handles conversion.

## Execute borrow

Confirm the asset, amount, chain, and projected health factor with the user. The `value` field must be `0x`-prefixed hex (typically `"0x0"` for ERC-20 borrows).

```bash
mm wallet send-transaction --chain-id <CHAIN_ID> --payload '{"to":"<TO>","value":"0x0","data":"<DATA>"}' --wait --intent "Borrow <AMOUNT> <SYMBOL> from Aave V3 on <CHAIN_NAME>"
```

If the response is `InsufficientBalanceError`, show the required and available amounts and stop.

## Notes

- After the transaction confirms, use `aave-positions.md` to verify the updated position and health factor.
- The borrowed amount accrues interest over time. Check debt at any time using `aave-positions.md`.
- To repay the borrow, see `aave-repay.md`.
