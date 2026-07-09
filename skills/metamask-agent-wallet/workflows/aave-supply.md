# Aave V3 supply

Use when the user wants to supply (deposit) an asset into Aave V3 to earn interest.
Withdrawing: workflows/aave-withdraw.md. Borrowing: workflows/aave-borrow.md.
Shared machinery (endpoint, response types, approval rule): references/aave.md.

## Preconditions

1. `mm doctor` reports `authenticated: true` and `initialized: true`. If not: SKILL.md § Preflight.
2. You know: chain, asset, amount. If the chain was not named, ask — do not guess.
   Resolve a symbol to a contract address: `mm token list search --query USDC --chain 8453 --toon`.
3. Balance covers the amount plus gas: `mm wallet balance --chain <chain-id>`. If not: offer a
   swap (workflows/swap.md) or bridge (workflows/bridge.md) first.

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

### 2. Get the sender address

```bash
mm wallet address --toon
```

Expected output: the active wallet address.
Capture: `address` → `<address>` (sender) in step 3.

### 3. Query the supply transaction

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ supply(request: { market: \"0xA238Dd80C259a72e81d7e4664a9801593F98d1c5\", amount: { erc20: { currency: \"0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913\", value: \"100\" } }, sender: \"0x7c2b3e65ef2b18235e2d24266f92854a70207483\", chainId: 8453 }) { __typename ... on TransactionRequest { to from data value chainId } ... on ApprovalRequired { reason requiredAmount { value decimals } currentAllowance { value decimals } approval { to from data value chainId } originalTransaction { to from data value chainId } } ... on InsufficientBalanceError { required { value decimals } available { value decimals } } } }"}'
```

Supply amount is a plain decimal string (references/aave.md § Amount format). Native-token
supply (only where the reserve accepts it): replace `erc20: { currency: ..., value: \"100\" }`
with `native: \"100\"`.
Expected output: `__typename` of `TransactionRequest`, `ApprovalRequired`, or
`InsufficientBalanceError` — handle per references/aave.md § Response types.
Capture: `to` and `data` (from `approval` and/or the transaction) → step 5 payload.

### 4. Confirm with the user

Show: asset symbol + contract address, amount, chain, pool address; if `ApprovalRequired`,
also the spender and that the API default allowance is UNLIMITED, offering the exact-amount
alternative (references/aave.md § Approval security rule). Do not continue until the user
explicitly approves. If `InsufficientBalanceError`: show `required` vs `available` and stop.

### 5. Execute — pick ONE branch for `value`

If the supplied asset is an ERC-20 → `"value":"0x0"` (`to`/`data` from step 3):

```bash
mm wallet send-transaction --chain-id 8453 --payload '{"to":"0xA238Dd80C259a72e81d7e4664a9801593F98d1c5","value":"0x0","data":"0x617ba037000000000000000000000000833589fcd6edb6e08f4c7c32d4f71b54bda02913"}' --wait --intent "Supply 100 USDC to Aave V3 on Base" --toon
```

If the supplied asset is the NATIVE token → `"value"` is the hex printed by
`python3 "$SKILL_DIR/scripts/amount_to_hex.py" 0.5 18` (→ `0x6f05b59d3b20000`):

```bash
mm wallet send-transaction --chain-id 8453 --payload '{"to":"0xA238Dd80C259a72e81d7e4664a9801593F98d1c5","value":"0x6f05b59d3b20000","data":"0x617ba0370000000000000000000000004200000000000000000000000000000000000006"}' --wait --intent "Supply 0.5 ETH to Aave V3 on Base" --toon
```

If step 3 returned `ApprovalRequired`: run this command first with the APPROVAL's `to`/`data`
(`"value":"0x0"`, intent "Approve 100 USDC for Aave V3 Pool on Base"), wait for completion,
then run it again with `originalTransaction`'s `to`/`data`.
Expected output: transaction completion (with `--wait`) or a `pollingId`
(references/concepts.md § Async job model).

## Decision points

- User rejects at step 4 → stop. Do not execute.
- User declines the unlimited approval → build exact-amount calldata with
  `scripts/encode_approve.py` (references/aave.md § Approval security rule).
- Asset missing from the market's reserves → offer workflows/aave-markets.md to pick a
  supported asset.
- After completion → verify the new aToken position via workflows/aave-positions.md.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| `InsufficientBalanceError` | Show `required` vs `available`; offer swap/bridge, then restart at step 3 |
| GraphQL `errors[]` in response | Re-check pool address, asset address, chain ID, amount format (references/aave.md) |
| `WALLET_ERROR` (gas) | `mm wallet balance --chain <chain-id>`; top up the native token |
