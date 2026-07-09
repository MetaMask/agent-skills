# Aave V3 markets and rates

Use when the user wants to discover which assets Aave V3 supports on a chain, their supply
and borrow APYs, or available borrow liquidity. Read-only — no transaction is sent. Feeds
workflows/aave-supply.md and workflows/aave-borrow.md. The user's own positions:
workflows/aave-positions.md. Shared machinery (endpoint): references/aave.md.

## Preconditions

1. `mm doctor` reports `authenticated: true` and `initialized: true`. If not: SKILL.md § Preflight.
2. You know the chain. If the chain was not named, ask — do not guess. Chain IDs: `mm chains list`.

## Steps

### 1. Query markets with reserve details

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ markets(request: { chainIds: [8453] }) { address reserves { underlyingToken { symbol decimals } supplyInfo { apy { formatted } } borrowInfo { apy { formatted } availableLiquidity { amount { value } usd } borrowCapReached } isFrozen isPaused } } }"}'
```

Expected output: `data.markets[]`, one entry per market, each with `address` (the pool
contract) and a `reserves[]` array.
Capture: `markets[].address` → `<pool-address>` for a follow-up supply/borrow workflow.

### 2. Present the results

1. Group reserves by market `address`; label each group with its pool address.
2. Drop reserves where `isFrozen` or `isPaused` is `true`.
3. For each remaining reserve show:
   - Symbol and decimals (`underlyingToken.symbol`, `underlyingToken.decimals`)
   - Supply APY (`supplyInfo.apy.formatted`)
   - Borrow APY (`borrowInfo.apy.formatted`)
   - Available liquidity (`borrowInfo.availableLiquidity.amount.value` and `.usd`)
   - Borrow cap reached (`borrowInfo.borrowCapReached`)
4. `apy.formatted` is already a percentage (`"2.12"` = 2.12%) — do not convert.

## Decision points

- `borrowCapReached` is `true` for an asset → tell the user borrowing that asset is
  unavailable; supplying may still work.
- User picks an asset to supply → workflows/aave-supply.md (reuse the captured `<pool-address>`).
- User picks an asset to borrow → workflows/aave-borrow.md (reuse the captured `<pool-address>`).
- Empty `markets[]` → Aave V3 not deployed on this chain; ask the user for another chain.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| GraphQL `errors[]` in response | Re-check the chain ID and query syntax against references/aave.md § Endpoint |
| Asset the user wants is missing or frozen/paused | Offer another asset from the list or another chain |
