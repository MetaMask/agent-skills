# Aave V3 repay

Use when the user wants to repay borrowed assets on Aave V3.
Borrowing: workflows/aave-borrow.md. Withdrawing collateral: workflows/aave-withdraw.md.
Shared machinery (endpoint, response types, approval rule): references/aave.md.

## Preconditions

1. `mm doctor` reports `authenticated: true` and `initialized: true`. If not: SKILL.md § Preflight.
2. You know: chain, asset, amount (or "full debt"). If the chain was not named, ask.
3. Outstanding debt exists — check `userBorrows` via workflows/aave-positions.md and show the
   user the debt amount (`debt.amount.value`) and borrow APY (`apy.formatted`).
4. Wallet balance covers the repayment plus gas: `mm wallet balance --chain <chain-id>`.

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

### 2. Query the repay transaction

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ repay(request: { market: \"0xA238Dd80C259a72e81d7e4664a9801593F98d1c5\", amount: { erc20: { currency: \"0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913\", value: { exact: \"100\" } } }, sender: \"0x7c2b3e65ef2b18235e2d24266f92854a70207483\", chainId: 8453 }) { __typename ... on TransactionRequest { to from data value chainId } ... on ApprovalRequired { reason requiredAmount { value decimals } currentAllowance { value decimals } approval { to from data value chainId } originalTransaction { to from data value chainId } } ... on InsufficientBalanceError { required { value decimals } available { value decimals } } } }"}'
```

Full debt: use `value: { max: true }` instead of `value: { exact: \"100\" }` — the contract
computes the exact debt (including accrued interest) at execution time. `{ max: true }` is
NOT allowed with `onBehalfOf`; when repaying for another address, use `exact` with the
current debt plus a small buffer (about 0.5%) — the contract refunds the excess.
Sender comes from `mm wallet address --toon`.
Expected output: `__typename` — handle per references/aave.md § Response types.
Capture: `to` and `data` (from `approval` and/or the transaction) → step 4 payload.

### 3. Confirm with the user

Show: asset symbol + contract address, amount (or "full debt"), chain, pool address; if
`ApprovalRequired`, also the spender and that the API default allowance is UNLIMITED,
offering the exact-amount alternative (references/aave.md § Approval security rule).
Do not continue until the user explicitly approves. If `InsufficientBalanceError`: show
`required` vs `available` and stop.

### 4. Execute

```bash
mm wallet send-transaction --chain-id 8453 --payload '{"to":"0xA238Dd80C259a72e81d7e4664a9801593F98d1c5","value":"0x0","data":"0x573ade81000000000000000000000000833589fcd6edb6e08f4c7c32d4f71b54bda02913"}' --wait --intent "Repay 100 USDC on Aave V3 on Base" --toon
```

`"value"` is `"0x0"` for ERC-20 repayments; `to`/`data` come from step 2. If step 2 returned
`ApprovalRequired`: send the APPROVAL's `to`/`data` first (`"value":"0x0"`, intent
"Approve 100 USDC for Aave V3 Pool on Base"), wait for completion, then send
`originalTransaction`'s `to`/`data`.
Expected output: transaction completion (with `--wait`) or a `pollingId`
(references/concepts.md § Async job model).

## Decision points

- User rejects at step 3 → stop. Do not execute.
- User wants the debt fully cleared → prefer `{ max: true }`; repaying the exact original
  borrow amount leaves interest "dust" that blocks full collateral withdrawal.
- Dust debt remains after an exact repay → re-run with `{ max: true }`, or over-repay with a
  0.5% buffer; if the wallet holds only the exact original amount, acquire slightly more first.
- Exact-amount approval already consumed by a prior repay → a new approval is required for
  the next repay.
- After completion → verify the debt is cleared or reduced via workflows/aave-positions.md.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| `InsufficientBalanceError` | Show `required` vs `available`; offer a swap (workflows/swap.md) or bridge (workflows/bridge.md), then restart at step 2 |
| GraphQL `errors[]` in response | Re-check pool address, asset address, chain ID, amount format (references/aave.md); `{ max: true }` with `onBehalfOf` is invalid |
| `WALLET_ERROR` (gas) | `mm wallet balance --chain <chain-id>`; top up the native token |
