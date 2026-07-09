# mm token

Read-only token discovery and metadata: search by symbol/name, curated lists, and CAIP-19
asset metadata (including security signals).

## Prerequisites

- `mm doctor` reports `authenticated: true` and `initialized: true` (SKILL.md § Preflight).
- Build CAIP-19 identifiers by string substitution — see references/concepts.md § CAIP identifiers.
- Multi-step discovery pattern (symbol → CAIP-19 → price): workflows/market-data.md.

## mm token list search

Search tokens by symbol or name across one or more chains. Read-only. This is the standard
way to resolve a symbol to a contract address.

### Syntax

```bash
mm token list search --query <query> [--chain <chain-id>] [--limit <n>] [--after <cursor>]
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--query` | symbol or name string | e.g. `USDC`, `Wrapped Ether` |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--chain` | active wallet chain, else `eip155:1` | comma-separated chain IDs or CAIP-2 IDs, no spaces (`1,137`) | Chains to search. Options: `mm token networks` |
| `--limit` | `10` | integer 1-500 | Maximum results |
| `--after` | — | cursor string | Pagination cursor: `nextCursor` from a previous response |

Global flags apply — see SKILL.md § Global flags.

### Output

```text
ok: true
data:
  query: USDC
  networks[1]: "eip155:1"
  tokens[2]{symbol,name,address,decimals,chainId,price,priceChangePct24h,marketCap,volume24hUsd}:
    USDC,USDC,0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48,6,"eip155:1",1.000022769440105,null,73203337961,11222199505
    AUSDC,Aave USDC,0xbcca60bb61934080951369a648fb03df4f96263c,6,"eip155:1",1.003,null,0,19337.26
  nextCursor: MQ==
  hasNextPage: true
```

Capture: `address` + `chainId` → build `<caip19>` as `<caip2>/erc20:<address>` for
`mm token assets`, `mm price spot`, and `mm price history`.

### Examples

```bash
mm token list search --query USDC --chain 1 --limit 2 --toon
mm token list search --query "Wrapped Ether" --chain 1,8453 --limit 5 --toon
```

## mm token list popular | trending | top-gainer

Curated token lists for one chain. Read-only. Three sibling commands with identical flags.

### Syntax

```bash
mm token list popular [--chain <chain-id>]
mm token list trending [--chain <chain-id>]
mm token list top-gainer [--chain <chain-id>]
```

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--chain` | active wallet chain, else `eip155:1` | chain ID or CAIP-2 ID (`1` or `eip155:1`) | Chain to list. Options: `mm token networks` |

Global flags apply — see SKILL.md § Global flags.

### Output

```text
ok: true
data:
  tokens[N]{symbol,name,address,decimals,chainId,price,priceChangePct24h,marketCap,volume24hUsd}: …
```
<!-- shape from CLI flag metadata; not a captured run -->

### Examples

```bash
mm token list popular --chain 1 --toon
mm token list trending --chain 137 --toon
mm token list top-gainer --chain 8453 --toon
```

## mm token assets

Fetch metadata for one or more CAIP-19 asset IDs. Read-only. Use `--include-token-security-data`
to surface scam/risk signals before the user trades an unfamiliar token.

### Syntax

```bash
mm token assets --asset-ids <caip19> [--include-market-data] [--include-token-security-data] [--include-labels] [--include-aggregators] [--include-coingecko-id] [--include-occurrences] [--include-rwa-data]
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--asset-ids` | one or more `<caip19>`, comma-separated, no spaces | Assets to describe (e.g. `eip155:1/erc20:0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48`) |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--include-market-data` | off | boolean flag | Market cap, volume, price data |
| `--include-token-security-data` | off | boolean flag | Security signals (scam risk, honeypot detection) |
| `--include-labels` | off | boolean flag | Token labels and categories |
| `--include-aggregators` | off | boolean flag | Aggregator sources listing the token |
| `--include-coingecko-id` | off | boolean flag | CoinGecko identifier |
| `--include-occurrences` | off | boolean flag | Occurrence count across chains |
| `--include-rwa-data` | off | boolean flag | Real-world asset data |

Global flags apply — see SKILL.md § Global flags.

### Output

```text
ok: true
data:
  assets[N]{assetId,symbol,name,decimals,…}: one row per requested asset ID
```
<!-- shape from CLI flag metadata; not a captured run -->

### Examples

```bash
mm token assets --asset-ids eip155:1/erc20:0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48 --include-market-data --include-token-security-data --toon
mm token assets --asset-ids eip155:1/slip44:60,eip155:137/erc20:0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359 --include-labels --toon
```

## mm token networks

List CAIP-2 networks supported by the Token API. Read-only.

### Syntax

```bash
mm token networks
```

No required or optional flags. Global flags apply — see SKILL.md § Global flags.

### Output

```text
ok: true
data:
  networks[N]: "eip155:1","eip155:10","eip155:56",…
```
<!-- shape from CLI flag metadata; not a captured run -->

### Examples

```bash
mm token networks --toon
```

## Errors

| Code | Cause | Recovery |
| --- | --- | --- |
| `INVALID_ASSET_ID` | Malformed `--asset-ids` value | Rebuild the CAIP-19 per references/concepts.md; get the address from `mm token list search` |
| `INVALID_CHAIN` | Chain not supported by the Token API | Run `mm token networks` and pick a listed chain |
| `INVALID_LIMIT` | `--limit` outside 1-500 | Re-run with an integer between 1 and 500 |
| `TOKEN_NOT_FOUND` | No token matches the query or asset ID | Broaden `--chain`, try an alternate symbol/name, or ask the user for the contract address |

Full code list: references/errors.md.
