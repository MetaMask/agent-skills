# Same-chain swap

Use when the user wants to swap one token for another on a single chain.
Cross-chain: use workflows/bridge.md instead. Command details: references/swap.md.

## Preconditions

1. `mm doctor` reports `authenticated: true` and `initialized: true`. If not: SKILL.md § Preflight.
2. You know: source token, destination token, amount, chain. If the chain was not named, ask —
   do not guess. List chains with `mm chains list`.
3. Balance covers the amount plus gas: `mm wallet balance --chain <chain-id>`.

## Steps

### 1. Get a quote

```bash
mm swap quote --from ETH --to USDC --amount 0.5 --from-chain 1 --toon
```

Do NOT pass `--to-chain`, `--to-address`, or `--refuel` for a same-chain swap. `--to-address`
is rejected same-chain (`INVALID_SWAP_PARAMS`) — output always goes to the active wallet.
Expected output: `data.quoteId` plus a `quote` object with `destAssetAmount`,
`minDestAssetAmount`, and `feeData`.
Capture: `quoteId` → used as `<quote-id>` in steps 3 and 4.

### 2. Confirm with the user

Show: from token, to token, amount, chain, slippage (default 0.5%), quoted output amount
(`destAssetAmount` scaled by the destination token's `decimals`), minimum received
(`minDestAssetAmount`), fees. Do not continue until the user explicitly approves.

### 3. Execute by quote id

```bash
mm swap execute --quote-id <quote-id> --toon
```

Always execute the reviewed quote by id. Never pass token/amount flags here — that re-quotes
and executes a price the user never reviewed.

### 4. Track status

```bash
mm swap status --quote-id <quote-id> --toon
```

Repeat until the status is terminal (completed or failed), then report the result.

## Decision points

- User rejects at step 2 → stop. Do not execute.
- Quote expired or not found at step 3 → return to step 1, then re-confirm at step 2.
- User wants the output at a different address → impossible same-chain; offer a follow-up
  `mm transfer` after the swap completes.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| `NO_QUOTES` | No route for this pair/amount. Try a different amount or token pair; verify the token exists on the chain with `mm token list search --query <symbol> --chain <chain-id>` |
| Insufficient balance | `mm wallet balance --chain <chain-id>`; offer a bridge from another chain (workflows/bridge.md) |
| User asks for higher slippage | Re-quote with `--slippage <percent>` only after explicit user approval; warn above 1% |
