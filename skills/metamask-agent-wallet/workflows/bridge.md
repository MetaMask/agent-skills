# Cross-chain bridge

Use when the user wants to move tokens from one chain to another.
Same-chain: use workflows/swap.md instead. Command details: references/swap.md.

## Preconditions

1. `mm doctor` reports `authenticated: true` and `initialized: true`. If not: SKILL.md § Preflight.
2. You know: source token, destination token, amount, source chain, destination chain. If a
   chain was not named, ask — do not guess. List chains with `mm chains list`.
3. Source-chain balance covers the amount plus gas: `mm wallet balance --chain <chain-id>`.

## Steps

### 1. Get a bridge quote

```bash
mm swap quote --from USDC --to USDC --amount 100 --from-chain 1 --to-chain 137 --toon
```

Cross-chain only, add as needed: `--to-address <address>` to send output to another wallet;
`--refuel` to bundle a destination native-gas top-up (skip it when the destination token IS
the destination chain's native gas asset — that route returns `NO_QUOTES`).
Expected output: `data.quoteId` plus a `quote` object with `destAssetAmount`,
`minDestAssetAmount`, `bridgeId`, and `feeData`.
Capture: `quoteId` → used as `<quote-id>` in steps 3 and 4.

### 2. Confirm with the user

Show: from token, to token, amount, source chain, destination chain, slippage (default 0.5%),
expected output (`destAssetAmount` scaled by the destination token's `decimals`), minimum
received (`minDestAssetAmount` scaled), fees, bridge route (`bridgeId`), recipient address
(only if `--to-address` was set), destination gas top-up (only if `--refuel` was set).
Do not continue until the user explicitly approves.

### 3. Execute by quote id

```bash
mm swap execute --quote-id <quote-id> --toon
```

Always execute the reviewed quote by id. Never pass token/amount flags here — that re-quotes
and executes a price the user never reviewed. The persisted quote already carries the
recipient and refuel settings.
Expected output: a wallet job (`pollingId`) — show its `intent` to the user.

### 4. Track status until terminal

```bash
mm swap status --quote-id <quote-id> --toon
```

Repeat until the status is terminal (completed or failed). The destination-chain side can lag
minutes behind the source transaction — keep polling; do not re-execute. Then report both
source and destination results.

## Decision points

- User rejects at step 2 → stop. Do not execute.
- Quote expired or `QUOTE_NOT_FOUND` at step 3 → return to step 1, then re-confirm at step 2.
- `NO_QUOTES` with `--refuel` → the destination token is likely the native gas asset; retry
  step 1 without `--refuel`.
- User wants output at a different address → valid only cross-chain via `--to-address`
  (same-chain it is rejected with `INVALID_SWAP_PARAMS`).
- Recipient may have no gas on the destination chain and destination token is non-native →
  offer `--refuel` before quoting.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| `NO_QUOTES` | No route for this pair/amount/chains. Drop `--refuel` if set; try a different amount or token; verify the token exists on both chains with `mm token list search --query USDC --chain 137` |
| `INVALID_SWAP_PARAMS` (`--to-address` same-chain) | Ensure `--to-chain` differs from `--from-chain`, or omit `--to-address` |
| Insufficient balance | `mm wallet balance --chain <chain-id>`; fund the source chain first, then re-quote |
| Slippage exceeded / user asks for higher slippage | Re-quote with `--slippage <percent>` only after explicit user approval; warn above 1% |
| Status stuck non-terminal | Keep polling `mm swap status`; destination settlement can take minutes. Do not re-execute |
