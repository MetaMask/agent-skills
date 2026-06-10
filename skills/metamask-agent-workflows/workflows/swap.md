# Swap workflow

Use this workflow when the user wants to swap tokens on the same chain.

Reference command syntax in `references/swap.md`.

## Flow

1. Quote.
2. Confirm with the user.
3. Execute and track status.

Don't skip the quote review step. The user needs to see output amount, fees, route, and slippage before executing.

## Quote

```bash
mm swap quote --from ETH --to USDC --amount 1 --from-chain 1
```

Required flags: `--from`, `--to`, `--amount`, and `--from-chain`.

If the user wants the output tokens sent to a different wallet, add `--to-address`:

```bash
mm swap quote --from ETH --to USDC --amount 1 --from-chain 1 --to-address 0x742d...f2bD18
```

Persist the quote id for execution. Show the quote to the user before execution.
Confirm source token, destination token, amount, chain, slippage, expected output, fees, route, and recipient address (if `--to-address` was set).

## Execute

```bash
mm swap execute --quote-id "$QUOTE_ID"
```

Prefer executing by quote ID. Re-quote-and-execute flags exist, but quote ID execution keeps the reviewed quote tied to the submitted action.

## Status

```bash
mm swap status --quote-id "$QUOTE_ID"
```

## Edge cases

- Quote expired: re-quote and ask the user to review the new quote.
- Insufficient balance: surface the error verbatim.
- Slippage exceeded: only increase `--slippage` if the user explicitly accepts more slippage. Always warn the user
  if slippage is increased above 1% that it will affect the minimum received.
- Missing chain: use `mm chains list` before guessing a chain ID.
