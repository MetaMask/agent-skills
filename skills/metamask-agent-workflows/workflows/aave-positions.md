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

If the user doesn't specify a chain, ask. Fetch all markets for the chain to get pool addresses:

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ markets(request: { chainIds: [<CHAIN_ID>] }) { address } }"}'
```

Collect all returned `address` values as `<POOL_ADDRESSES>`.

## Query positions

Query supply and borrow positions across all markets in a single request. Build the `markets` array from all addresses returned above:

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "{ userSupplies(request: { markets: [{ address: \"<POOL_ADDRESS_1>\", chainId: <CHAIN_ID> }, { address: \"<POOL_ADDRESS_2>\", chainId: <CHAIN_ID> }], user: \"<WALLET_ADDRESS>\" }) { currency { symbol decimals } balance { amount { value } usd } apy { formatted } isCollateral marketAddress } userBorrows(request: { markets: [{ address: \"<POOL_ADDRESS_1>\", chainId: <CHAIN_ID> }, { address: \"<POOL_ADDRESS_2>\", chainId: <CHAIN_ID> }], user: \"<WALLET_ADDRESS>\" }) { currency { symbol decimals } debt { amount { value } usd } apy { formatted } marketAddress } }"
  }'
```

Include one `{ address, chainId }` entry per market returned by the previous query. The response contains both `userSupplies` and `userBorrows` arrays spanning all markets.

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