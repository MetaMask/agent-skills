# Aave V3 collateral toggle

Use when the user wants to enable or disable a supplied asset as collateral on Aave V3.
Supplying: workflows/aave-supply.md. Repaying debt first: workflows/aave-repay.md.
Shared machinery (endpoint, executing, confirm rule): references/aave.md.

## Preconditions

1. `mm doctor` reports `authenticated: true` and `initialized: true`. If not: SKILL.md § Preflight.
2. You know: chain and asset. If the chain was not named, ask — do not guess.
   Resolve a symbol to a contract address: `mm token list search --query USDC --chain 8453 --toon`.
3. The wallet has a non-zero supply of the asset on Aave (check via workflows/aave-positions.md);
   toggling collateral on an unsupplied asset reverts.

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

### 2. Get the sender address and current status

```bash
mm wallet address --toon
```

Expected output: the active wallet address.
Capture: `address` → `<address>` in step 3.
Then run the positions query (workflows/aave-positions.md § Steps 3) and read the target
asset's `isCollateral` field — this tells you which direction the toggle will take.

### 3. Query the collateral toggle transaction

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ collateralToggle(request: { market: \"0xA238Dd80C259a72e81d7e4664a9801593F98d1c5\", underlyingToken: \"0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913\", user: \"0x7c2b3e65ef2b18235e2d24266f92854a70207483\", chainId: 8453 }) { to from data value chainId } }"}'
```

The toggle direction is decided by the API from the current on-chain state.
Expected output: a `TransactionRequest` `{to, from, data, value, chainId}`.
Capture: `to` and `data` → step 5 payload.

### 4. Confirm with the user

Show: asset symbol + contract address, chain, pool address, and the toggle direction
(enabling or disabling, from step 2's `isCollateral`). If DISABLING and the user has any
borrows: show the current health factor and warn that disabling lowers it; if it would drop
below 1.0, stop and point to workflows/aave-repay.md. Do not continue until the user
explicitly approves.

### 5. Execute the toggle

```bash
mm wallet send-transaction --chain-id 8453 --payload '{"to":"0xA238Dd80C259a72e81d7e4664a9801593F98d1c5","value":"0x0","data":"0x5a3b74b9000000000000000000000000833589fcd6edb6e08f4c7c32d4f71b54bda029130000000000000000000000000000000000000000000000000000000000000001"}' --wait --intent "Enable USDC as collateral on Aave V3 on Base" --toon
```

Use the `to`/`data` captured in step 3 (`"value"` is always `"0x0"` for a toggle).
Expected output: transaction completion (with `--wait`) or a `pollingId`
(references/concepts.md § Async job model).

### 6. Verify

Re-run the positions query (workflows/aave-positions.md) and confirm the asset's
`isCollateral` flipped as expected.

## Decision points

- User rejects at step 4 → stop. Do not execute.
- Asset has zero supplied balance → offer workflows/aave-supply.md first.
- Disabling would push the health factor below 1.0 → stop; offer workflows/aave-repay.md.
- Transaction reverts → the reserve may not be collateral-eligible; check the market's
  reserves via workflows/aave-markets.md.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| GraphQL `errors[]` in response | Re-check pool address, asset address, chain ID (references/aave.md) |
| On-chain revert | Asset not supplied, or reserve not collateral-eligible; verify via workflows/aave-positions.md and workflows/aave-markets.md |
| `WALLET_ERROR` (gas) | `mm wallet balance --chain <chain-id>`; top up the native token |
