# mm price

Read-only spot prices, historical prices, and price-API capability lists for CAIP-19 assets.

## Prerequisites

- `mm doctor` reports `authenticated: true` and `initialized: true` (SKILL.md § Preflight).
- Build CAIP-2 / CAIP-19 identifiers by string substitution — see references/concepts.md § CAIP identifiers.
- Unknown token contract address? Resolve it first with `mm token list search` (references/token.md).

## mm price spot

Fetch current prices for one or more CAIP-19 assets. Read-only.

### Syntax

```bash
mm price spot --asset-ids <caip19> [--vs <currency>] [--market-data]
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--asset-ids` | one or more `<caip19>`, comma-separated, no spaces | Assets to price (e.g. `eip155:1/slip44:60,eip155:1/erc20:0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48`) |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--vs` | `usd` | currency code from `mm price currencies` | Quote currency |
| `--market-data` | off | boolean flag | Include market cap, supply, and 24h change |

Global flags apply — see SKILL.md § Global flags.

### Output

```text
ok: true
data:
  vsCurrency: usd
  includeMarketData: false
  prices[1]{assetId,vsCurrency,price}:
    "eip155:1/slip44:60",usd,1741.75
```

### Examples

```bash
# ETH and POL native prices in USD
mm price spot --asset-ids eip155:1/slip44:60,eip155:137/slip44:966 --toon
# USDC on Ethereum with market data, in EUR
mm price spot --asset-ids eip155:1/erc20:0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48 --vs eur --market-data --toon
```

## mm price history

Fetch historical prices for one CAIP-19 asset. Read-only. The asset is split across two flags:
`--chain-id` takes the CAIP-2 part, `--asset-type` takes the part after the `/`.

### Syntax

```bash
mm price history --chain-id <caip2> --asset-type <asset-type> [--time-period <period>] [--interval <interval>] [--from <unix>] [--to <unix>] [--vs <currency>]
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--chain-id` | `<caip2>` (e.g. `eip155:1`) | Chain. Supported chains: `mm price networks` |
| `--asset-type` | `slip44:<coin>` or `erc20:<address>` | The CAIP-19 asset type (the part after `/`) |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--time-period` | API default | `1d`, `7d`, `30d`, `2M`, `1y`, `3y` | Lookback window. Do not combine with `--from`/`--to` |
| `--from` | — | `<unix>` seconds | Custom range start; use together with `--to` |
| `--to` | — | `<unix>` seconds | Custom range end; use together with `--from` |
| `--interval` | API default | `5m`, `hourly`, `daily` | Sampling interval |
| `--vs` | `usd` | currency code from `mm price currencies` | Quote currency |

Global flags apply — see SKILL.md § Global flags.

### Output

```text
ok: true
data:
  chainId: "eip155:1"
  assetType: "slip44:60"
  vsCurrency: usd
  timePeriod: 1d
  interval: daily
  prices[2]:
    - [2]: 1783555200000,1742.5277253393804
    - [2]: 1783609607000,1739.5050996130065
  marketCaps[2]: …
  totalVolumes[2]: …
```

`prices` rows are `[millisecond-timestamp, price]` pairs.

### Examples

```bash
# ETH daily prices over the last 7 days
mm price history --chain-id eip155:1 --asset-type slip44:60 --time-period 7d --interval daily --toon
# USDC on Ethereum for a custom Unix range
mm price history --chain-id eip155:1 --asset-type erc20:0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48 --from 1783000000 --to 1783600000 --interval hourly --toon
```

## mm price currencies

List supported quote currencies for `--vs`. Read-only.

### Syntax

```bash
mm price currencies
```

No required or optional flags. Global flags apply — see SKILL.md § Global flags.

### Output

```text
ok: true
data:
  currencies[94]: btc,eth,ltc,bch,bnb,eos,xrp,xlm,link,dot,yfi,usd,aed,ars,aud,…
```

### Examples

```bash
mm price currencies --toon
```

## mm price networks

List CAIP-2 networks supported by the price API. Read-only.

### Syntax

```bash
mm price networks
```

No required or optional flags. Global flags apply — see SKILL.md § Global flags.

### Output

```text
ok: true
data:
  fullSupport[11]: "eip155:1","eip155:10","eip155:56","eip155:100","eip155:137","eip155:250","eip155:324","eip155:8453","eip155:42161","eip155:43114","eip155:59144"
  partialSupport:
    spotPricesV2[68]: "eip155:25","eip155:30",…
    spotPricesV3[72]: "eip155:25","eip155:30",…
```

### Examples

```bash
mm price networks --toon
```

## Errors

| Code | Cause | Recovery |
| --- | --- | --- |
| `INVALID_ASSET_ID` | Malformed `--asset-ids` value | Rebuild the CAIP-19 per references/concepts.md; resolve contract addresses with `mm token list search` |
| `INVALID_CHAIN` | Chain not supported by the price API | Run `mm price networks` and pick a listed CAIP-2 ID |
| `INVALID_INTERVAL` | `--interval` not one of `5m`, `hourly`, `daily` | Re-run with a listed interval |
| `INVALID_TIMESTAMP` | `--from`/`--to` not Unix seconds, or from > to | Regenerate with `date +%s`; ensure `--from` < `--to` |

Full code list: references/errors.md.
