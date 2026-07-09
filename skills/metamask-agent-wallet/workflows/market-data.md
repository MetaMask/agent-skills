# Token discovery and market data

Use when the user asks for a token's price, price history, or metadata and you do not yet have
its CAIP-19 asset ID. Already have the CAIP-19 (or it is a native asset like ETH)? Skip to
step 3. Command details: references/price.md and references/token.md.

## Preconditions

1. `mm doctor` reports `authenticated: true` and `initialized: true`. If not: SKILL.md § Preflight.
2. You know the chain. If the user did not name one, ask — do not guess. Chain IDs:
   `mm chains list`; token-API coverage: `mm token networks`.

## Steps

### 1. Resolve the token to a contract address

Native assets (ETH, POL) need no search — build `eip155:<chain-id>/slip44:<coin>` directly
(references/concepts.md § CAIP identifiers) and skip to step 3. For any other symbol or name:

```bash
mm token list search --query USDC --chain 1 --limit 5 --toon
```

Expected output: `data.tokens` rows with `symbol`, `name`, `address`, `decimals`, `chainId`.
Capture: `address` + `chainId` → build `<caip19>` as `<caip2>/erc20:<address>`, e.g.
`eip155:1/erc20:0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48`.

### 2. Disambiguate

If more than one row plausibly matches the user's request (same or similar symbol), show the
user the candidates (symbol, name, address, market cap) and ask which one they mean. Do not
pick silently.

### 3. Get the spot price

```bash
mm price spot --asset-ids eip155:1/erc20:0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48 --market-data --toon
```

Expected output: `data.prices` rows with `assetId`, `vsCurrency`, `price`.

### 4. Get historical prices (only if the user asked for a trend or range)

Split the CAIP-19: the part before `/` goes to `--chain-id`, the part after to `--asset-type`.

```bash
mm price history --chain-id eip155:1 --asset-type erc20:0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48 --time-period 7d --interval daily --toon
```

Expected output: `data.prices` rows of `[millisecond-timestamp, price]` pairs.

## Decision points

- Search returns zero rows → retry with more chains (`--chain 1,137,8453`) or an alternate
  name; still nothing → ask the user for the contract address.
- Multiple plausible matches → ask the user (step 2). Never assume the first row.
- User wants a curated browse instead of a specific token → `mm token list popular|trending|top-gainer --chain <chain-id>` (references/token.md).
- User wants safety/metadata detail → `mm token assets --asset-ids <caip19> --include-token-security-data --include-market-data`.
- User names a non-USD currency → check it exists via `mm price currencies`, then add `--vs <currency>`.
- Custom date range → replace `--time-period` with `--from <unix> --to <unix>` (`date +%s`).

## Errors

| Error / symptom | Recovery |
| --- | --- |
| `INVALID_ASSET_ID` | Rebuild the CAIP-19 per references/concepts.md; re-check the address from step 1 |
| `INVALID_CHAIN` | Chain not covered by the API; run `mm price networks` / `mm token networks` and pick a listed chain |
| `TOKEN_NOT_FOUND` | Broaden the search chains or ask the user for the contract address |
| Price looks stale or null | Retry with `--market-data`; for thin tokens warn the user that pricing may be unreliable |
