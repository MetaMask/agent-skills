# mm predict (market data)

Browse Polymarket data: markets, events, series, tags, and order books. All commands in this
file are read-only and need no confirmation.

## Prerequisites

- `mm doctor` reports `authenticated: true` and `initialized: true` (SKILL.md § Preflight).
- No Predict setup needed to browse. Setup gate applies only to trading
  (references/predict-trade.md) and funding (references/predict-account.md).
- Flow: find a market (`markets search` or `markets list`) → `markets get` to read outcome
  token IDs → `book` / references/predict-trade.md with those `<token-id>` values.
- Tag slugs/IDs from `tags list` feed the `--tag`/`--tag-slug`/`--tag-id` filters below.

## mm predict markets list

List tradeable Predict markets with Gamma-style filters. Read-only.

### Syntax

```bash
mm predict markets list [--limit <limit>] [--tag <tag-slug>] [--active] [--closed]
```

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--slug` | omitted | market slug string | Filter by market slug |
| `--limit` | server default | integer 1-500 | Maximum markets to return |
| `--offset` | `0` | integer ≥ 0 | Result offset for pagination |
| `--order` | omitted | comma-separated field names | Market fields to order by |
| `--ascending` | off | boolean flag | Sort ascending (default descending) |
| `--tag` | omitted | tag slug string | Market tag or category (e.g. `sports`, `politics`) |
| `--liquidity-num-min` | omitted | decimal | Minimum market liquidity |
| `--liquidity-num-max` | omitted | decimal | Maximum market liquidity |
| `--volume-num-min` | omitted | decimal | Minimum market volume |
| `--volume-num-max` | omitted | decimal | Maximum market volume |
| `--start-date-min` | omitted | ISO 8601 date-time | Minimum market start date-time |
| `--start-date-max` | omitted | ISO 8601 date-time | Maximum market start date-time |
| `--end-date-min` | omitted | ISO 8601 date-time | Minimum market end date-time |
| `--end-date-max` | omitted | ISO 8601 date-time | Maximum market end date-time |
| `--active` | off | boolean flag | Only include active markets |
| `--closed` | off | boolean flag | Include closed markets |

Global flags apply — see SKILL.md § Global flags.

### Output

List of market objects with `id`, `question`, `conditionId`, `slug`, `outcomes`,
`outcomePrices`, `liquidity`, `volume`, `active`, `closed` (same shape as the captured
`markets search` output below).
<!-- shape from CLI flag metadata; not a captured run -->

Capture: `slug` or `conditionId` → use in `mm predict markets get --market <condition-id>`.

### Examples

```bash
mm predict markets list --tag sports --liquidity-num-min 10000 --limit 10 --toon
mm predict markets list --active --limit 50 --toon
```

## mm predict markets search

Free-text search via Polymarket public search. Read-only. The query is POSITIONAL — there is
no query flag.

### Syntax

```bash
mm predict markets search <query> [--limit <limit>]
```

`<query>` is a search string; quote it if it contains spaces. (New placeholder: `<query>`.)

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--limit` | `10` | integer | Results per type |
| `--page` | `1` | integer | Search result page |
| `--sort` | omitted | field name | Search sort field |
| `--ascending` | off | boolean flag | Sort ascending |
| `--search-tags` | on | boolean flag | Include tag matches (`--no-search-tags` to disable) |
| `--events-status` | active | boolean flag | Restrict to active events (`--no-events-status` for all) |
| `--recurrence` | omitted | `annual`\|`daily`\|`weekly`\|`monthly` | Filter by series recurrence |

Global flags apply — see SKILL.md § Global flags.

### Output

```yaml
ok: true
data:
  command: "market:search"
  params: {query: bitcoin, limit: 1, searchTags: true, eventsStatus: active}
  result:
    markets[11]:
      - id: "2769746"
        question: "Will the price of Bitcoin be above $52,000 on July 9?"
        conditionId: 0x5179f59617e32ce893c4ecc0ee1e4916c65f7a85eb3774c87cdc3430cb1d0d73
        slug: bitcoin-above-52k-on-july-9-2026
        outcomes: "[\"Yes\", \"No\"]"
        outcomePrices: "[\"0.9995\", \"0.0005\"]"
        liquidity: "210307.34108"
        active: true
        closed: false
        orderPriceMinTickSize: 0.001
        orderMinSize: 5
```

Capture: `slug` or `conditionId` → use in `mm predict markets get --market <condition-id>`.

### Examples

```bash
mm predict markets search bitcoin --limit 1 --toon
mm predict markets search "Knicks NBA Finals" --limit 5 --toon
```

## mm predict markets get

Inspect one market and read the outcome token IDs required by quote/place/book/balance. Read-only.

### Syntax

```bash
mm predict markets get --market <slug>
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--market` | market slug, ID, or `<condition-id>` | The market to inspect (find via `markets search`/`markets list`) |

Global flags apply — see SKILL.md § Global flags. (New placeholder: `<slug>`.)

### Output

Market object with `question`, `conditionId`, per-outcome token IDs, prices, tick size, and
minimum order size.
<!-- shape from CLI flag metadata; not a captured run -->

Capture: outcome token ID → use as `<token-id>` in `mm predict book --token-id <token-id>` and
references/predict-trade.md; `conditionId` → `<condition-id>` for cancel/redeem.

### Examples

```bash
mm predict markets get --market bitcoin-above-52k-on-july-9-2026 --toon
mm predict markets get --market 0x5179f59617e32ce893c4ecc0ee1e4916c65f7a85eb3774c87cdc3430cb1d0d73 --toon
```

## mm predict events list / events get

List Polymarket events (groupings of related markets), or inspect one. Read-only.
`events get` is positional-only.

### Syntax

```bash
mm predict events list [--tag-slug <tag-slug>] [--active] [--limit <limit>]
mm predict events get <event>
```

`<event>` is an event slug or ID. (New placeholder: `<event>`.)

### Optional flags (events list only; events get has none)

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--tag-slug` | omitted | tag slug string | Filter by tag slug (e.g. `sports`) |
| `--tag-id` | omitted | integer | Filter by tag ID (from `mm predict tags list`) |
| `--active` | off | boolean flag | Active events only |
| `--closed` | off | boolean flag | Include closed/resolved events |
| `--featured` | off | boolean flag | Only featured/trending events |
| `--order` | omitted | `volume_24hr`\|`volume`\|`liquidity`\|`start_date`\|`end_date` | Sort field |
| `--ascending` | off | boolean flag | Sort ascending (default descending) |
| `--liquidity-min` | omitted | decimal | Minimum event liquidity |
| `--start-date-min` / `--start-date-max` | omitted | ISO 8601 | Event start date bounds |
| `--end-date-min` / `--end-date-max` | omitted | ISO 8601 | Event end date bounds |
| `--limit` | server default | integer | Max results |
| `--offset` | `0` | integer ≥ 0 | Result offset for pagination |

Global flags apply — see SKILL.md § Global flags.

### Output

Event objects with `id`, `slug`, `title`, and nested market summaries.
<!-- shape from CLI flag metadata; not a captured run -->

### Examples

```bash
mm predict events list --tag-slug sports --limit 10 --toon
mm predict events get us-recession-in-2026 --toon
```

## mm predict series list / series get

List recurring Polymarket event series, or inspect one by ID. Read-only. `series get` is
positional-only.

### Syntax

```bash
mm predict series list [--recurrence <recurrence>] [--limit <limit>]
mm predict series get <series-id>
```

(New placeholders: `<recurrence>`, `<series-id>`.)

### Optional flags (series list only; series get has none)

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--recurrence` | omitted | `annual`\|`daily`\|`weekly`\|`monthly` | Filter by recurrence |
| `--active` | off | boolean flag | Active series only |
| `--featured` | off | boolean flag | Only featured series |
| `--tag-slug` | omitted | tag slug string | Filter by tag slug |
| `--limit` | server default | integer | Max results |
| `--offset` | `0` | integer ≥ 0 | Result offset for pagination |

Global flags apply — see SKILL.md § Global flags.

### Output

Series objects with `id`, `slug`, `title`, `recurrence`.
<!-- shape from CLI flag metadata; not a captured run -->

### Examples

```bash
mm predict series list --recurrence weekly --limit 10 --toon
mm predict series get 12345 --toon
```

## mm predict tags list / tags get

List Polymarket tags (feed `--tag`/`--tag-slug`/`--tag-id` filters), or fetch one by ID or
slug. Read-only. `tags get` is positional-only.

### Syntax

```bash
mm predict tags list [--limit <limit>]
mm predict tags get <tag-slug>
```

`<tag-slug>` for `tags get` may also be a numeric tag ID. (New placeholder: `<tag-slug>`.)

### Optional flags (tags list only; tags get has none)

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--limit` | server default | integer | Max results |
| `--offset` | `0` | integer ≥ 0 | Result offset for pagination |
| `--is-carousel` | off | boolean flag | Only carousel tags |

Global flags apply — see SKILL.md § Global flags.

### Output

```yaml
ok: true
data:
  command: tags
  params: {limit: 3}
  result:
    tags[3]:
      - id: "101867"
        label: product marekt fit
        slug: product-marekt-fit
      - id: "1512"
        label: caitlin clark
        slug: caitlin-clark
      - id: "100601"
        label: virgins
        slug: virgins
```

Capture: `slug` → `--tag-slug`/`--tag`; `id` → `--tag-id`.

### Examples

```bash
mm predict tags list --limit 3 --toon
mm predict tags get sports --toon
```

## mm predict book

Fetch the raw order book for an outcome token. Read-only.

### Syntax

```bash
mm predict book --token-id <token-id>
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--token-id` | outcome token ID string | From `mm predict markets get --market <slug>` |

Global flags apply — see SKILL.md § Global flags.

### Output

Bids and asks as `{price, size}` levels; prices are per-share in the range (0, 1].
<!-- shape from CLI flag metadata; not a captured run -->

### Examples

```bash
mm predict book --token-id 21742633143463906290569050155826241533067272736897614950488156847949938836455 --toon
```

## Errors

| Code | Cause | Recovery |
| --- | --- | --- |
| `ValidationError` | Malformed flag value or missing positional argument | Re-check values against the tables above |
| `NOT_FOUND` | Unknown slug, ID, condition ID, or token ID | Re-discover via `mm predict markets search <query>` or `mm predict tags list` |
| `UNKNOWN` (`fetch failed`) | Transient network failure to Gamma/CLOB | Retry; check reachability with `mm predict status` (references/predict-account.md) |

Full code list: references/errors.md.
