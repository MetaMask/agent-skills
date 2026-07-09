# Aave V3 borrow

Use when the user wants to borrow assets from Aave V3 against supplied collateral.
Supplying collateral: workflows/aave-supply.md. Repaying: workflows/aave-repay.md.
Shared machinery (endpoint, response types, executing): references/aave.md.

## Preconditions

1. `mm doctor` reports `authenticated: true` and `initialized: true`. If not: SKILL.md § Preflight.
2. You know: chain, asset, amount. If the chain was not named, ask — do not guess.
3. The user has supplied collateral with `isCollateral: true` on at least one asset — verify
   via workflows/aave-positions.md. No collateral → workflows/aave-supply.md; collateral
   disabled → workflows/aave-collateral.md.
4. The asset is borrowable: `borrowCapReached` is `false` and the reserve is not frozen or
   paused — check via workflows/aave-markets.md.

## Steps

### 1. Discover the market (pool address)

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ markets(request: { chainIds: [8453] }) { address reserves { underlyingToken { symbol } } } }"}'
```

Expected output: `data.markets[]` with `address` and reserve symbols. Multiple markets → ask
the user which one (references/aave.md § Market discovery).
Capture: `markets[].address` → `<pool-address>`.

### 2. Preview health factor

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ healthFactorPreview(request: { action: { borrow: { market: \"0xA238Dd80C259a72e81d7e4664a9801593F98d1c5\", sender: \"0x7c2b3e65ef2b18235e2d24266f92854a70207483\", chainId: 8453, amount: { erc20: { currency: \"0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913\", value: \"100\" } } } } }) { before after } }"}'
```

Expected output: `data.healthFactorPreview.before` and `.after`. Sender comes from
`mm wallet address --toon`.
If `after` < 1.5 → warn about liquidation risk. If `after` < 1.0 → stop; suggest a smaller
amount or repaying existing debt.

### 3. Query the borrow transaction

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ borrow(request: { market: \"0xA238Dd80C259a72e81d7e4664a9801593F98d1c5\", amount: { erc20: { currency: \"0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913\", value: \"100\" } }, sender: \"0x7c2b3e65ef2b18235e2d24266f92854a70207483\", chainId: 8453 }) { __typename ... on TransactionRequest { to from data value chainId } ... on ApprovalRequired { approval { to from data value chainId } originalTransaction { to from data value chainId } } ... on InsufficientBalanceError { required { value decimals } available { value decimals } } } }"}'
```

Borrow amount is a plain decimal string (references/aave.md § Amount format). Do NOT include
`onBehalfOf` for a self-borrow — it triggers a credit-delegation requirement.
Expected output: `__typename` — handle per references/aave.md § Response types.
Capture: `to` and `data` → step 5 payload.

### 4. Confirm with the user

Show: asset symbol + contract address, amount, chain, pool address, borrow APY (from
workflows/aave-markets.md if known), and the projected health factor from step 2. Remind
that debt accrues interest. Do not continue until the user explicitly approves.

### 5. Execute

```bash
mm wallet send-transaction --chain-id 8453 --payload '{"to":"0xA238Dd80C259a72e81d7e4664a9801593F98d1c5","value":"0x0","data":"0xa415bcad000000000000000000000000833589fcd6edb6e08f4c7c32d4f71b54bda02913"}' --wait --intent "Borrow 100 USDC from Aave V3 on Base" --toon
```

`"value"` is `"0x0"` for borrows; `to`/`data` come from step 3.
Expected output: transaction completion (with `--wait`) or a `pollingId`
(references/concepts.md § Async job model).

## Decision points

- User rejects at step 4 → stop. Do not execute.
- Projected health factor below 1.0 at step 2 → stop; offer a smaller amount or more collateral.
- `borrowCapReached` is `true` for the asset → borrowing unavailable; suggest another asset.
- After completion → verify debt and health factor via workflows/aave-positions.md; repayment
  via workflows/aave-repay.md.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| `InsufficientBalanceError` | Borrow capacity too low; show `required` vs `available`, suggest more collateral or a smaller amount |
| GraphQL `errors[]` in response | Re-check pool address, asset address, chain ID, amount format (references/aave.md); ensure no `onBehalfOf` |
| `WALLET_ERROR` (gas) | `mm wallet balance --chain <chain-id>`; top up the native token |
