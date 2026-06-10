# Aave V3 collateral workflow

Use this workflow to enable or disable an asset as collateral on Aave V3.

## Flow

1. Resolve chain, asset address, and pool address.
2. Check current collateral status and health factor.
3. Query the Aave API for the collateral toggle transaction.
4. Execute toggle.

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

## Check status

Query the user's positions using `aave-positions.md`. For the target asset, check whether collateral is enabled or disabled (`isCollateral`).

The user must have a non-zero supply of the asset to toggle collateral.

When disabling collateral, check the health factor. If the user has outstanding borrows, disabling collateral lowers the health factor. Show the impact. If the health factor would drop below 1.0, stop and tell the user to repay debt first via `aave-repay.md`.

## Query collateral toggle transaction

Get the wallet address and query the Aave V3 GraphQL API:

```bash
mm wallet address
```

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "{ collateralToggle(request: { market: \"<POOL_ADDRESS>\", underlyingToken: \"<ASSET_ADDRESS>\", user: \"<WALLET_ADDRESS>\", chainId: <CHAIN_ID> }) { to from data value chainId } }"
  }'
```

The API returns a `TransactionRequest` with `{to, from, data, value, chainId}`. The toggle direction is determined automatically based on the current collateral state.

## Execute toggle

Confirm the asset, toggle direction (enabling or disabling), and chain with the user. The `value` field must be `0x`-prefixed hex.

```bash
mm wallet send-transaction --chain-id <CHAIN_ID> --payload '{"to":"<TO>","value":"0x0","data":"<DATA>"}' --wait --intent "Toggle <SYMBOL> as collateral on Aave V3 on <CHAIN_NAME>"
```

## Notes

- Enabling collateral lets the asset back borrows, increasing borrow capacity.
- Disabling collateral removes it from the borrow calculation. This may trigger liquidation if remaining collateral can't cover existing debt.
- Not all assets support collateral usage. If the transaction reverts, the reserve may not be eligible.
- After the transaction confirms, verify the updated status using `aave-positions.md`.
