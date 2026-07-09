# mm predict (trading)

Quote, place, cancel, and track Predict (Polymarket) orders; view positions, portfolio, and
redeem winnings.

## Prerequisites

- `mm doctor` reports `authenticated: true` and `initialized: true` (SKILL.md § Preflight).
- Setup gate: `mm predict status` shows `account.setupComplete: true`
  (references/predict-account.md). Otherwise every command here fails `PREDICT_SETUP_REQUIRED`.
- pUSD funds the orders: check `mm predict balance --sync`, top up with `mm predict deposit`
  (references/predict-account.md).
- `<token-id>` and `<condition-id>` come from `mm predict markets get --market <slug>`
  (references/predict-data.md).
- Prices are per-share, in the range (0, 1]. Sides are `buy` or `sell`. Order types: `GTC`
  (limit, default), `GTD` (limit with `--expiration`), `FOK`/`FAK` (market-style).

## mm predict quote

Preview order cost and fill before placing. Read-only.

### Syntax

```bash
mm predict quote --token-id <token-id> --side <side> --size <size> [--limit-price <price>]
```

(New placeholders: `<side>` = `buy`|`sell`, `<size>` = shares decimal, `<price>` = decimal in (0, 1].)

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--token-id` | outcome token ID string | From `mm predict markets get` |
| `--side` | `buy` \| `sell` | Order side |
| `--size` | decimal `^\d+\.?\d*$`, > 0 | Order size in shares (`1`, `100`) |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--limit-price` | market price | decimal in (0, 1] | Execution price per share |

Global flags apply — see SKILL.md § Global flags. BYOK with an encrypted mnemonic: set
`MM_PASSWORD` first (references/concepts.md).

### Output

Estimated cost, average fill price, and fillable size for the requested order.
<!-- shape from CLI flag metadata; not a captured run -->

### Examples

```bash
mm predict quote --token-id 21742633143463906290569050155826241533067272736897614950488156847949938836455 --side buy --size 10 --toon
mm predict quote --token-id 21742633143463906290569050155826241533067272736897614950488156847949938836455 --side sell --size 5 --limit-price 0.60 --toon
```

## mm predict place

Place a Predict order (GTC/GTD limit, FOK/FAK market). State-changing.

### Syntax

```bash
mm predict place --token-id <token-id> --side <side> --size <size> --price <price> [--order-type <order-type>] [--post-only] [--expiration <unix>]
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--token-id` | outcome token ID string | From `mm predict markets get` |
| `--side` | `buy` \| `sell` | Order side |
| `--size` | decimal `^\d+\.?\d*$`, > 0 | Order size in shares |
| `--price` | decimal in (0, 1] | Worst price per share: limit price for GTC/GTD, worst fill for FOK/FAK |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--order-type` | `GTC` | `GTC` \| `GTD` \| `FOK` \| `FAK` | Order type |
| `--post-only` | off | boolean flag | Reject if the order would cross the book. Not valid with FOK/FAK |
| `--expiration` | none | `<unix>` seconds (`date +%s`) | Required for GTD; invalid for other types |

Global flags apply — see SKILL.md § Global flags. BYOK with an encrypted mnemonic: set
`MM_PASSWORD` first (references/concepts.md).

### Output

Order record with `orderId` and status, or a job ID for asynchronous submission.
<!-- shape from CLI flag metadata; not a captured run -->

Capture: `orderId` → use as `<order-id>` in `mm predict cancel --order-id <order-id>`; a job
ID → `<polling-id>` in `mm predict watch --id <polling-id> --wait`.

### Async

If a job ID is returned, track it with `mm predict watch --id <polling-id> --wait`.

### Confirm before executing

Show the user ALL of: market question, outcome, side, size (shares), price per share,
order type, total cost (size × price for buys), expiration if GTD. Do not run until the
user approves. Quote first with `mm predict quote`.

### Examples

```bash
mm predict place --token-id 21742633143463906290569050155826241533067272736897614950488156847949938836455 --side buy --size 10 --price 0.55 --toon
mm predict place --token-id 21742633143463906290569050155826241533067272736897614950488156847949938836455 --side sell --size 2 --price 0.70 --order-type GTD --expiration 1783600000 --toon
```

## mm predict cancel

Cancel open Predict orders. State-changing. Pass EXACTLY ONE targeting flag:

- If the user names one order → `--order-id <order-id>`.
- If the user wants everything cancelled → `--all` (destructive scope — confirm explicitly).
- If the user wants one market cleared → `--market <condition-id>`.
- If the user wants one outcome token cleared → `--asset <token-id>`.

### Syntax

```bash
mm predict cancel --order-id <order-id>
```

### Optional flags (exactly one required)

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--order-id` | — | order ID string | Cancel a single order |
| `--all` | — | boolean flag | Cancel ALL open orders |
| `--market` | — | `<condition-id>` (`0x` + 64 hex) | Cancel all orders in one market |
| `--asset` | — | outcome token ID string | Cancel all orders on one outcome token |

Global flags apply — see SKILL.md § Global flags. BYOK with an encrypted mnemonic: set
`MM_PASSWORD` first (references/concepts.md).

### Output

List of cancelled order IDs.
<!-- shape from CLI flag metadata; not a captured run -->

### Async

Completes inline; no `pollingId`.

### Confirm before executing

Show the user the exact scope: the order ID, or "ALL open orders", or the market/asset being
cleared plus how many open orders match (`mm predict orders`). Do not run until approved.

### Examples

```bash
mm predict cancel --order-id 0x1f9090aae28b8a3dceadf281b0f12828e676c326 --toon
mm predict cancel --market 0x5179f59617e32ce893c4ecc0ee1e4916c65f7a85eb3774c87cdc3430cb1d0d73 --toon
```

## mm predict orders

View open Predict orders. Read-only.

### Syntax

```bash
mm predict orders [--market <condition-id>] [--cursor <cursor>]
```

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--market` | all markets | market slug, ID, or `<condition-id>` | Filter to one market |
| `--cursor` | first page | cursor string from a previous response | Pagination |

Global flags apply — see SKILL.md § Global flags. BYOK with an encrypted mnemonic: set
`MM_PASSWORD` first (references/concepts.md).

### Output

Open orders with `orderId`, token, side, size, price, and a pagination `cursor`.
<!-- shape from CLI flag metadata; not a captured run -->

Capture: `orderId` → `<order-id>` for `mm predict cancel --order-id <order-id>`.

### Examples

```bash
mm predict orders --toon
```

## mm predict positions

View Predict positions. Read-only.

### Syntax

```bash
mm predict positions [--market <condition-id>]
```

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--market` | all markets | market slug, ID, or `<condition-id>` | Filter to one market |

Global flags apply — see SKILL.md § Global flags. BYOK with an encrypted mnemonic: set
`MM_PASSWORD` first (references/concepts.md).

### Output

Positions with market question, outcome, size, and estimated value.
<!-- shape from CLI flag metadata; not a captured run -->

### Examples

```bash
mm predict positions --toon
```

## mm predict portfolio

Full snapshot: pUSD balance, open positions with estimated value, redeemable winnings. Read-only.
No command-specific flags besides the pointer line below.

### Syntax

```bash
mm predict portfolio
```

Global flags apply — see SKILL.md § Global flags. BYOK with an encrypted mnemonic: set
`MM_PASSWORD` first (references/concepts.md).

### Output

`{"ok": true, "data": {"result": {"balance": "...", "positions": [], "redeemable": []}}}`
<!-- shape from CLI flag metadata; not a captured run -->

### Examples

```bash
mm predict portfolio --toon
```

## mm predict redeem list

List all redeemable (winning) positions with size and market question. Read-only.
No command-specific flags.

### Syntax

```bash
mm predict redeem list
```

Global flags apply — see SKILL.md § Global flags. BYOK with an encrypted mnemonic: set
`MM_PASSWORD` first (references/concepts.md).

### Output

Redeemable positions with `conditionId`, market question, and size.
<!-- shape from CLI flag metadata; not a captured run -->

Capture: `conditionId` → `<condition-id>` for `mm predict redeem <condition-id> --wait`.

### Examples

```bash
mm predict redeem list --toon
```

## mm predict redeem

Redeem winning tokens after market resolution. State-changing. Choose EXACTLY ONE form:

- If the user names one market → positional: `mm predict redeem <condition-id> [--wait]`.
- If the user wants everything → `mm predict redeem --all [--wait]` (destructive scope — confirm explicitly).

### Syntax

```bash
mm predict redeem <condition-id> [--wait]
```

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--all` | off | boolean flag | Redeem all redeemable positions (replaces the positional) |
| `--wait` | off | boolean flag | Block until the redemption transaction is confirmed |

Global flags apply — see SKILL.md § Global flags. BYOK with an encrypted mnemonic: set
`MM_PASSWORD` first (references/concepts.md).

### Output

`{"ok": true, "data": {"result": {"pollingId": "..."}}}`
<!-- shape from CLI flag metadata; not a captured run -->

Capture: `pollingId` → `<polling-id>` for `mm predict watch --id <polling-id> --wait`.

### Async

Without `--wait`, track the job with `mm predict watch --id <polling-id> --wait`.

### Confirm before executing

Show the user: the market(s) being redeemed (from `mm predict redeem list`) and the expected
pUSD proceeds; for `--all`, list every affected market. Do not run until approved.

### Examples

```bash
mm predict redeem 0x5179f59617e32ce893c4ecc0ee1e4916c65f7a85eb3774c87cdc3430cb1d0d73 --wait --toon
mm predict redeem --all --wait --toon
```

## mm predict watch

Watch a setup, approval, deposit, withdraw, or order job until it completes. Read-only tracker.

### Syntax

```bash
mm predict watch --id <polling-id> [--wait]
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--id` | job or transaction ID string | The `pollingId` returned by a Predict state-changing command |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--wait` | off | boolean flag | Block until the job completes (prefer this) |

Global flags apply — see SKILL.md § Global flags. BYOK with an encrypted mnemonic: set
`MM_PASSWORD` first (references/concepts.md).

### Output

Job status record; terminal states report success/failure and any transaction hash.
<!-- shape from CLI flag metadata; not a captured run -->

### Examples

```bash
mm predict watch --id 018f9a2b-4c6d-7e8f-9a0b-1c2d3e4f5a6b --wait --toon
```

## Errors

| Code | Cause | Recovery |
| --- | --- | --- |
| `PREDICT_SETUP_REQUIRED` | Setup incomplete for the owner EOA | `mm predict setup --wait`, verify with `mm predict status` (references/predict-account.md) |
| `PREDICT_GEOBLOCKED` | Restricted region | `mm predict geoblock`; Predict unavailable from this IP |
| `ValidationError` | Price outside (0, 1], `--post-only` with FOK/FAK, `--expiration` without GTD, or multiple/zero cancel targets | Fix the flag combination per the tables above |
| `WALLET_ERROR` | Insufficient pUSD for the order | `mm predict balance --sync`; deposit via references/predict-account.md |
| `UNKNOWN` (`fetch failed`) | Transient CLOB/Gamma network failure | Retry; check `mm predict status` |

Full code list: references/errors.md.
