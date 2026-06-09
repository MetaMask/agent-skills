# Aave V3 positions workflow

Use this workflow to check Aave V3 positions, health factor, interest rates, or reserve data.

## Flow

1. Get wallet address and chain.
2. Query supply and borrow positions via GraphQL.
3. Present summary.

## Resolve chain

Get the wallet address:

```bash
mm wallet address
```

If the user doesn't specify a chain, ask. Aave V3 is deployed on these chains:

| Chain | Chain ID | Pool address |
| --- | --- | --- |
| Ethereum | 1 | `0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2` |
| Polygon | 137 | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` |
| Arbitrum | 42161 | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` |
| Optimism | 10 | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` |
| Avalanche | 43114 | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` |
| Base | 8453 | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` |

## Query positions

Query supply and borrow positions in a single request:

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "{ userSupplies(request: { markets: [{ address: \"<POOL_ADDRESS>\", chainId: <CHAIN_ID> }], user: \"<WALLET_ADDRESS>\" }) { currency { symbol decimals } balance { amount { value } usd } apy { formatted } isCollateral } userBorrows(request: { markets: [{ address: \"<POOL_ADDRESS>\", chainId: <CHAIN_ID> }], user: \"<WALLET_ADDRESS>\" }) { currency { symbol decimals } debt { amount { value } usd } apy { formatted } } }"
  }'
```

The response contains both `userSupplies` and `userBorrows` arrays.

## Health factor preview

Preview the health factor impact of a planned operation:

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "{ healthFactorPreview(request: { action: { <OPERATION>: { market: \"<POOL_ADDRESS>\", sender: \"<WALLET_ADDRESS>\", chainId: <CHAIN_ID>, amount: { erc20: { currency: \"<ASSET_ADDRESS>\", value: \"<AMOUNT>\" } } } } }) { before after } }"
  }'
```

Replace `<OPERATION>` with `supply`, `borrow`, `withdraw`, or `repay`. All action types require `market`, `sender`, and `chainId`.

## Present summary

Format the data into three sections:

Supplied assets:
- Symbol, balance (`balance.amount.value`), USD value (`balance.usd`), supply APY (`apy.formatted`), used as collateral (`isCollateral`)

Borrowed assets:
- Symbol, debt amount (`debt.amount.value`), USD value (`debt.usd`), borrow APY (`apy.formatted`)

Account summary:
- Total collateral value, total debt value, available borrows, health factor
- Health factor guidance: above 2.0 is safe, 1.5–2.0 is moderate, 1.0–1.5 is risky and approaching liquidation, below 1.0 is liquidatable

The `apy.formatted` field returns a percentage directly (e.g., `"2.12"` means 2.12%). No conversion is needed.