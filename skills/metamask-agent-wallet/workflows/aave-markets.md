# Aave V3 markets workflow

Use this workflow to discover available Aave V3 tokens, supply/borrow rates, and borrowing capacity on a chain.

## Flow

1. Resolve chain.
2. Query available markets.
3. Present results.

## Resolve chain

If the user doesn't specify a chain, ask.

## Query available markets

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "{ markets(request: { chainIds: [<CHAIN_ID>] }) { address reserves { underlyingToken { symbol decimals } supplyInfo { apy { formatted } } borrowInfo { apy { formatted } availableLiquidity { amount { value } usd } borrowCapReached } isFrozen isPaused } } }"
  }'
```

The response returns one entry per market. Each entry has an `address` (the pool contract address) and a `reserves` array.

## Present results

Group reserves by market `address`. Within each market, filter out reserves where `isFrozen` or `isPaused` is `true`. For each active reserve, show:

- Token symbol and decimals (`underlyingToken.symbol`, `underlyingToken.decimals`)
- Supply APY (`supplyInfo.apy.formatted`)
- Borrow APY (`borrowInfo.apy.formatted`)
- Available liquidity (`borrowInfo.availableLiquidity.amount.value`, `borrowInfo.availableLiquidity.usd`)
- Borrow cap reached (`borrowInfo.borrowCapReached`)

The `apy.formatted` field returns a percentage directly (e.g., `"2.12"` means 2.12%). No conversion is needed.

If `borrowCapReached` is `true`, tell the user that borrowing isn't available for that asset.
