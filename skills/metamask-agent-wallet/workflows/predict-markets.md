# Browse prediction markets

Use when the user wants to find, browse, or inspect Polymarket prediction markets or read an
order book. Placing an order: workflows/predict-place-order.md. Command details:
references/predict-data.md.

## Preconditions

1. `mm doctor` reports `authenticated: true` and `initialized: true`. If not: SKILL.md § Preflight.
   No Predict setup is needed to browse — these commands are all read-only.
2. You know what the user is looking for (topic, question, or market). If not, ask.

## Steps

### 1. Search for markets

```bash
mm predict markets search "bitcoin above 52k" --limit 5 --toon
```

The query is positional — there is no query flag; quote multi-word queries.
Expected output: `result.markets[]` with `question`, `slug`, `conditionId`, `outcomes`,
`outcomePrices`, `liquidity`, `active`. Search can return loosely related markets — always
inspect the chosen market in step 2 before trading.
Capture: `slug` or `conditionId` → `<slug>` for step 2.

### 2. Inspect the chosen market

```bash
mm predict markets get --market bitcoin-above-52k-on-july-9-2026 --toon
```

Expected output: market detail with per-outcome token IDs, prices, tick size, and minimum
order size. Outcome token IDs are NOT market IDs — map the user's intended outcome (e.g.
"Yes") to its token ID.
Capture: outcome token ID → `<token-id>` for step 3 and for quote/place
(references/predict-trade.md); `conditionId` → `<condition-id>` for cancel/redeem.

### 3. Read the order book (optional)

```bash
mm predict book --token-id 21742633143463906290569050155826241533067272736897614950488156847949938836455 --toon
```

Expected output: bids and asks as `{price, size}` levels; prices are per-share in (0, 1].
Use the best bid/ask to suggest a realistic limit price.

## Decision points

- Search results are noisy → `mm predict markets list --active --limit 50 --toon` and filter
  manually, or narrow with `--tag <tag-slug>` (get slugs from `mm predict tags list --toon`).
- User wants to browse by topic instead of a specific question →
  `mm predict events list --tag-slug sports --active --limit 10 --toon`, then
  `mm predict events get <event> --toon`; events/series/tags do not return token IDs, so
  always finish with step 2 on a specific market.
- User picks a market and wants to trade → workflows/predict-place-order.md with the captured
  `<token-id>`.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| `NOT_FOUND` | Unknown slug/ID/token ID; re-run step 1 and re-copy the exact value |
| Empty search results | Broaden the query or raise `--limit`; try `markets list --active` |
| `UNKNOWN` (`fetch failed`) | Transient Gamma/CLOB failure; retry, check `mm predict status` |
