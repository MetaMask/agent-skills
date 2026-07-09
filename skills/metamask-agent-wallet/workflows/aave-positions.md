# Aave V3 positions and health factor

Use when the user wants to see their Aave V3 supplies, borrows, collateral status, or health
factor, or to preview the health-factor impact of a planned operation. Read-only — no
transaction is sent. Rates and available assets: workflows/aave-markets.md.
Shared machinery (endpoint, market discovery): references/aave.md.

## Preconditions

1. `mm doctor` reports `authenticated: true` and `initialized: true`. If not: SKILL.md § Preflight.
2. You know the chain. If the chain was not named, ask — do not guess. Chain IDs: `mm chains list`.

## Steps

### 1. Get the wallet address

```bash
mm wallet address --toon
```

Expected output: the active wallet address.
Capture: `address` → `<address>` in step 3.

### 2. Discover the markets (pool addresses)

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ markets(request: { chainIds: [8453] }) { address } }"}'
```

Expected output: `data.markets[]` with one `address` per market.
Capture: ALL `markets[].address` values → the `markets` array entries in step 3.

### 3. Query supplies and borrows across all markets

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ userSupplies(request: { markets: [{ address: \"0xA238Dd80C259a72e81d7e4664a9801593F98d1c5\", chainId: 8453 }], user: \"0x7c2b3e65ef2b18235e2d24266f92854a70207483\" }) { currency { symbol decimals } balance { amount { value } usd } apy { formatted } isCollateral marketAddress } userBorrows(request: { markets: [{ address: \"0xA238Dd80C259a72e81d7e4664a9801593F98d1c5\", chainId: 8453 }], user: \"0x7c2b3e65ef2b18235e2d24266f92854a70207483\" }) { currency { symbol decimals } debt { amount { value } usd } apy { formatted } marketAddress } }"}'
```

Include one `{ address, chainId }` entry per market captured in step 2.
Expected output: `userSupplies[]` and `userBorrows[]` arrays spanning all markets.

### 4. (Only if the user is planning an operation) Preview the health factor

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ healthFactorPreview(request: { action: { borrow: { market: \"0xA238Dd80C259a72e81d7e4664a9801593F98d1c5\", sender: \"0x7c2b3e65ef2b18235e2d24266f92854a70207483\", chainId: 8453, amount: { erc20: { currency: \"0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913\", value: \"100\" } } } } }) { before after } }"}'
```

The action key is one of `supply`, `borrow`, `withdraw`, `repay`; its `amount` uses the same
format as the wrapped operation (references/aave.md § Amount format).
Expected output: `healthFactorPreview` with `before` and `after`.

### 5. Present the summary

1. Supplied assets: symbol, `balance.amount.value`, `balance.usd`, `apy.formatted`, `isCollateral`.
2. Borrowed assets: symbol, `debt.amount.value`, `debt.usd`, `apy.formatted`.
3. Health factor with a risk label (see Decision points). `apy.formatted` is already a
   percentage (`"2.12"` = 2.12%) — do not convert.

## Decision points

- Health factor above 2.0 → safe; no warning needed.
- 1.5–2.0 → moderate; mention it when the user plans to borrow or withdraw more.
- 1.0–1.5 → risky, approaching liquidation; warn and offer workflows/aave-repay.md or
  workflows/aave-supply.md (more collateral).
- Below 1.0 → position is liquidatable; warn urgently and recommend immediate repay/supply.
- No supplies and no borrows returned → tell the user they have no Aave position on this
  chain; offer workflows/aave-markets.md and workflows/aave-supply.md.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| GraphQL `errors[]` in response | Re-check pool addresses, chain ID, and wallet address; re-run step 2 |
| Empty `markets[]` in step 2 | Aave V3 not deployed on this chain; ask the user for another chain |
