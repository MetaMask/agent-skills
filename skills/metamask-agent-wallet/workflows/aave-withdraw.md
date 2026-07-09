# Aave V3 withdraw

Use when the user wants to withdraw supplied assets from Aave V3.
Supplying: workflows/aave-supply.md. Repaying debt: workflows/aave-repay.md.
Shared machinery (endpoint, response types, executing): references/aave.md.

## Preconditions

1. `mm doctor` reports `authenticated: true` and `initialized: true`. If not: SKILL.md § Preflight.
2. You know: chain, asset, amount (or "full balance"). If the chain was not named, ask.
3. The user has a supply position in the asset — verify via workflows/aave-positions.md.
4. Full withdrawal only: `userBorrows` shows NO outstanding debt (even dust). If debt exists,
   the transaction reverts with `0x6679996d` — repay first via workflows/aave-repay.md.

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

### 2. Preview health factor (only if the user has outstanding borrows)

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ healthFactorPreview(request: { action: { withdraw: { market: \"0xA238Dd80C259a72e81d7e4664a9801593F98d1c5\", sender: \"0x7c2b3e65ef2b18235e2d24266f92854a70207483\", chainId: 8453, amount: { erc20: { currency: \"0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913\", value: { exact: \"100\" } } } } } }) { before after } }"}'
```

Expected output: `data.healthFactorPreview.before` and `.after`.
If `after` < 1.5 → warn about liquidation risk. If `after` < 1.0 → stop; the user must repay
debt first. Sender comes from `mm wallet address --toon`.

### 3. Query the withdraw transaction

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ withdraw(request: { market: \"0xA238Dd80C259a72e81d7e4664a9801593F98d1c5\", amount: { erc20: { currency: \"0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913\", value: { exact: \"100\" } } }, sender: \"0x7c2b3e65ef2b18235e2d24266f92854a70207483\", chainId: 8453 }) { __typename ... on TransactionRequest { to from data value chainId } ... on ApprovalRequired { approval { to from data value chainId } originalTransaction { to from data value chainId } } ... on InsufficientBalanceError { required { value decimals } available { value decimals } } } }"}'
```

Full balance: use `value: { max: true }` instead of `value: { exact: \"100\" }`.
To send funds to a different address, add `recipient: \"<address>\"` to the request.
Expected output: `__typename` — handle per references/aave.md § Response types.
Capture: `to` and `data` → step 5 payload.

### 4. Confirm with the user

Show: asset symbol + contract address, amount (or "full balance"), destination (default:
sender), chain, pool address, and the health-factor impact from step 2 if computed. Do not
continue until the user explicitly approves.

### 5. Execute

```bash
mm wallet send-transaction --chain-id 8453 --payload '{"to":"0xA238Dd80C259a72e81d7e4664a9801593F98d1c5","value":"0x0","data":"0x69328dec000000000000000000000000833589fcd6edb6e08f4c7c32d4f71b54bda02913"}' --wait --intent "Withdraw 100 USDC from Aave V3 on Base" --toon
```

`"value"` is `"0x0"` for withdrawals; `to`/`data` come from step 3. If step 3 returned
`ApprovalRequired`, send `approval` first, then `originalTransaction`
(references/aave.md § Response types).
Expected output: transaction completion (with `--wait`) or a `pollingId`
(references/concepts.md § Async job model).

## Decision points

- User rejects at step 4 → stop. Do not execute.
- Full withdrawal requested but debt exists → repay via workflows/aave-repay.md, then restart.
- Projected health factor below 1.0 at step 2 → stop; suggest a smaller amount or repaying debt.
- After completion → verify the reduced position via workflows/aave-positions.md.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| Revert `0x6679996d` | Outstanding debt blocks full withdrawal; clear ALL debt (workflows/aave-repay.md), then retry |
| `InsufficientBalanceError` | Requested more than supplied; show `required` vs `available`, ask for a smaller amount |
| GraphQL `errors[]` in response | Re-check pool address, asset address, chain ID, amount format (references/aave.md) |
| `WALLET_ERROR` (gas) | `mm wallet balance --chain <chain-id>`; top up the native token |
