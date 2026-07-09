# mm perps

Trade perpetual futures. Only venue: `hyperliquid`. Funds live in a venue account (deposit
USDC from Arbitrum first), separate from the wallet's on-chain balances.

## Prerequisites

- `mm doctor` reports `authenticated: true` and `initialized: true` (SKILL.md § Preflight).
- Shared optional flags, valid on every command below and omitted from the per-command tables:
  `--venue <venue>` (default `hyperliquid`, only allowed value `hyperliquid`) and `--network
  <network>` (default `mainnet`, allowed `mainnet` | `testnet`). Exception: `list-venues` takes
  neither. Include `--venue hyperliquid` in commands anyway for explicitness.
- The seven state-changing commands (`open`, `close`, `modify`, `cancel`, `deposit`,
  `withdraw`, `transfer`) additionally share these optional flags (also omitted from tables):
  `--dry-run` (preview without signing or submitting) and `--yes` (skip the interactive
  confirmation prompt — pass only after the user approved).
- Async model for the state-changing commands: the wallet job runs synchronously — no `--wait`
  flag, no `pollingId`. Global flags and `--wallet-timeout` apply — see SKILL.md § Global
  flags. BYOK with an encrypted mnemonic: set `MM_PASSWORD` first (references/concepts.md).
- Read-only commands (`list-venues`, `dexs`, `markets`, `balance`, `positions`, `orders`,
  `quote`): global flags apply — see SKILL.md § Global flags.
- `--size` is in the base asset (`0.01` = 0.01 BTC); deposit/withdraw/transfer amounts are USDC.

## mm perps list-venues

List available perpetual venues. Read-only. No flags beyond global.

### Syntax

```bash
mm perps list-venues
```

### Output

```
ok: true
data:
  venues[1]:
    - id: hyperliquid
      label: Hyperliquid
      networks[2]: mainnet,testnet
```

## mm perps dexs

List DEX identifiers a venue exposes (main Hyperliquid DEX is the empty string, plus HIP-3
DEXs). Read-only. No flags beyond the shared `--venue`/`--network`.

### Syntax

```bash
mm perps dexs --venue hyperliquid
```

### Output

```
ok: true
data:
  dexs[10]: "",xyz,flx,vntl,hyna,km,abcd,cash,para,mkts
```

## mm perps markets

List perpetual markets for a venue. Read-only.

### Syntax

```bash
mm perps markets --venue hyperliquid [--symbol <symbol>]
```

### Required flags

None.

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--symbol` | all markets | market symbol | Filter to a single market (e.g. `BTC`) |
| `--symbols` | all markets | comma-separated symbols | Filter to several markets (e.g. `BTC,ETH,SOL`) |
| `--dex` | main DEX | name from `mm perps dexs` | HIP-3 DEX name; omit for the main Hyperliquid DEX |

### Output

```
ok: true
data[1]{venue,symbol,maxLeverage,sizeDecimals,markPrice,oraclePrice,fundingRate,openInterest,volume24h}:
  hyperliquid,BTC,40,5,"62944.0","62961.0","0.0000125","37908.9644999999","1770767064.72…"
```

Capture: `symbol` → `<symbol>`; check `maxLeverage` before choosing `--leverage`.

## mm perps balance

Show the venue account's balances. Read-only. No flags beyond the shared `--venue`/`--network`.

### Syntax

```bash
mm perps balance --venue hyperliquid
```

### Output

```
ok: true
data:
  venue: hyperliquid
  totalBalance: "0.000042"
  spendableBalance: "0.000042"
  withdrawableBalance: "0.000042"
  marginUsed: "0"
  unrealizedPnl: "0.00"
  returnOnEquity: "0"
  subAccounts:
    main: …
```

## mm perps positions

List open positions. Read-only. No flags beyond the shared `--venue`/`--network`.

### Syntax

```bash
mm perps positions --venue hyperliquid
```

### Output

```
ok: true
data: []
```

Non-empty: one row per position (symbol, side, size, entry price, leverage, liquidation
price, unrealized PnL). Capture: `symbol` → `<symbol>` for `mm perps close` / `mm perps modify`.

## mm perps orders

List resting (unfilled) orders. Read-only. No flags beyond the shared `--venue`/`--network`.

### Syntax

```bash
mm perps orders --venue hyperliquid
```

### Output

```
ok: true
data: []
```

Non-empty rows include the venue order ID. Capture: order ID → `<order-id>` for `mm perps cancel`.

## mm perps quote

Estimate entry price, notional, fees, and liquidation price without placing an order. Read-only.

### Syntax

```bash
mm perps quote --venue hyperliquid --symbol <symbol> --side <side> --size <size> --leverage <leverage>
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--symbol` | market symbol | Market symbol (e.g. `BTC`, `ETH`, `SOL`) |
| `--side` | `long` or `short` | Position direction |
| `--size` | decimal `^\d+\.?\d*$`, > 0 | Size in base asset (e.g. `0.01`) |
| `--leverage` | positive integer | Leverage multiplier (e.g. `5`); ≤ market `maxLeverage` |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--type` | `market` | `market` or `limit` | Order type |
| `--limit-px` | — | decimal price | Limit price; required when `--type limit` |

### Output

```
ok: true
data:
  venue: hyperliquid
  symbol: BTC
  side: long
  orderType: market
  entryPrice: "62948"
  size: "0.001"
  notional: "62.95"
  estimatedFee: "0.0283"
  estimatedLiquidationPrice: "31474"
  feeRate: "0.00045"
  warnings[1]: Liquidation price is an estimate and does not include all venue-specific margin rules.
```

Capture: `entryPrice`, `notional`, `estimatedFee`, `estimatedLiquidationPrice` → show in the
confirmation before `mm perps open`.

## mm perps open

Open a new perpetual position by placing an order. State-changing.

### Syntax

```bash
mm perps open --venue hyperliquid --symbol <symbol> --side <side> --size <size> --leverage <leverage> [--type <order-type>] [--limit-px <price>] [--dry-run] [--yes]
```

### Required flags

Same four as `mm perps quote`: `--symbol`, `--side`, `--size`, `--leverage` (same formats).

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--type` | `market` | `market` or `limit` | Order type |
| `--limit-px` | — | decimal price | Limit price; required when `--type limit` |
| `--max-slippage-bps` | venue default | positive integer | Slippage cap in basis points for IOC market pricing (e.g. `50`) |

### Output

```json
{"ok": true, "data": {"status": "filled", "symbol": "BTC", "size": "0.001"}}
```
<!-- shape from CLI flag metadata; not a captured run -->

### Confirm before executing

Show ALL of: symbol, side, size, leverage, venue, order type, limit price (if limit), and the
quoted `entryPrice`, `notional`, `estimatedFee`, `estimatedLiquidationPrice` from
`mm perps quote`. Do not run until the user approves.

### Examples

```bash
mm perps open --venue hyperliquid --symbol BTC --side long --size 0.001 --leverage 2 --dry-run --toon
mm perps open --venue hyperliquid --symbol BTC --side long --size 0.001 --leverage 2 --yes --toon
mm perps open --venue hyperliquid --symbol ETH --side short --size 1 --leverage 10 --type limit --limit-px 2500 --yes --toon
```

## mm perps close

Close one position, part of one, or all open positions. State-changing.

### Syntax

Two disjoint modes — if closing one symbol use the first form; if closing everything, the second:

```bash
mm perps close --venue hyperliquid --symbol <symbol> [--size <size>] [--dry-run] [--yes]
mm perps close --venue hyperliquid --all [--dry-run] [--yes]
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--symbol` XOR `--all` | market symbol / boolean flag | `--symbol` closes one market; `--all` closes every open position. Mutually exclusive; exactly one required. |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--size` | full close | decimal, > 0 | Partial close size in base asset. Not allowed with `--all`. |
| `--max-slippage-bps` | venue default | positive integer | Slippage cap in basis points for IOC pricing |

### Output

```json
{"ok": true, "data": {"status": "filled", "symbol": "BTC", "closedSize": "0.001"}}
```
<!-- shape from CLI flag metadata; not a captured run -->

### Confirm before executing

Show ALL of: symbol (or "ALL open positions" for `--all`), size (full or partial), the
position's unrealized PnL from `mm perps positions`, venue. Do not run until the user approves.

### Examples

```bash
mm perps close --venue hyperliquid --symbol BTC --yes --toon
mm perps close --venue hyperliquid --symbol BTC --size 0.0005 --yes --toon
mm perps close --venue hyperliquid --all --dry-run --toon
```

## mm perps modify

Modify leverage, take-profit, or stop-loss on an existing position. State-changing.

### Syntax

```bash
mm perps modify --venue hyperliquid --symbol <symbol> [--leverage <leverage>] [--tp <price>] [--sl <price>] [--dry-run] [--yes]
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--symbol` | market symbol | Market symbol of the open position |

At least one of `--leverage`, `--tp`, `--sl` is also required.

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--leverage` | unchanged | positive integer | New leverage multiplier |
| `--tp` | unchanged | decimal price | Take-profit trigger price |
| `--sl` | unchanged | decimal price | Stop-loss trigger price |

### Output

```json
{"ok": true, "data": {"symbol": "BTC", "leverage": 10}}
```
<!-- shape from CLI flag metadata; not a captured run -->

### Confirm before executing

Show ALL of: symbol, venue, and each field being changed as old → new (leverage, TP, SL). Do
not run until the user approves.

### Examples

```bash
mm perps modify --venue hyperliquid --symbol BTC --leverage 10 --yes --toon
mm perps modify --venue hyperliquid --symbol ETH --tp 3000 --sl 2000 --yes --toon
```

## mm perps cancel

Cancel a resting perpetual order by venue order ID. State-changing.

### Syntax

```bash
mm perps cancel --venue hyperliquid --order-id <order-id> [--symbol <symbol>] [--dry-run] [--yes]
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--order-id` | positive integer | Venue order ID from `mm perps orders` |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--symbol` | looked up | market symbol | Speeds up cancel by avoiding the open-order lookup |

### Output

```json
{"ok": true, "data": {"orderId": 12345, "status": "cancelled"}}
```
<!-- shape from CLI flag metadata; not a captured run -->

### Confirm before executing

Show ALL of: order ID, plus that order's symbol, side, size, and price from `mm perps orders`.
Do not run until the user approves.

### Examples

```bash
mm perps cancel --venue hyperliquid --order-id 12345 --symbol BTC --yes --toon
```

## mm perps deposit

Deposit USDC from the wallet's on-chain balance into a perpetual venue. State-changing.

### Syntax

```bash
mm perps deposit --venue hyperliquid --amount <amount> [--dry-run] [--yes]
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--amount` | decimal, > 0 | Human-readable USDC amount (e.g. `100`) |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--asset` | `USDC` | `USDC` | Deposit asset (only USDC allowed) |
| `--source-chain` | Arbitrum for the network (`eip155:42161` on mainnet) | `<caip2>` | Source chain of the funds |

### Output

```json
{"ok": true, "data": {"amount": "100", "asset": "USDC", "status": "submitted"}}
```
<!-- shape from CLI flag metadata; not a captured run -->

Venue credit can take a few minutes; verify with `mm perps balance`.

### Confirm before executing

Show ALL of: amount, asset (USDC), source chain, venue. Verify the wallet holds the USDC plus
gas on the source chain first (`mm wallet balance --chain 42161`). Do not run until the user
approves.

### Examples

```bash
mm perps deposit --venue hyperliquid --amount 100 --yes --toon
```

## mm perps withdraw

Withdraw USDC from a perpetual venue to an EVM address. State-changing.

### Syntax

```bash
mm perps withdraw --venue hyperliquid --amount <amount> [--destination <address>] [--include-spot] [--dry-run] [--yes]
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--amount` | decimal, > 0 | Human-readable USDC amount (e.g. `50`) |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--asset` | `USDC` | `USDC` | Withdrawal asset (only USDC allowed) |
| `--destination` | connected wallet | `^0x[0-9a-fA-F]{40}$` | EVM destination address |
| `--include-spot` | off | boolean flag | Move free spot USDC to perp first if needed to cover the amount |

### Output

```json
{"ok": true, "data": {"amount": "50", "asset": "USDC", "status": "submitted"}}
```
<!-- shape from CLI flag metadata; not a captured run -->

### Confirm before executing

Show ALL of: amount, destination address (explicit or "connected wallet"), venue, whether
`--include-spot` is set. Verify `withdrawableBalance` covers the amount (`mm perps balance`).
Do not run until the user approves.

### Examples

```bash
mm perps withdraw --venue hyperliquid --amount 50 --yes --toon
mm perps withdraw --venue hyperliquid --amount 50 --destination 0x7c2b3e65ef2b18235e2d24266f92854a70207483 --include-spot --yes --toon
```

## mm perps transfer

Move USDC between spot and perp accounts inside the venue. State-changing.

### Syntax

```bash
mm perps transfer --venue hyperliquid --amount <amount> --direction <direction> [--dry-run] [--yes]
```

### Required flags

| Flag | Value format | Description |
| --- | --- | --- |
| `--amount` | decimal, > 0 | Human-readable USDC amount |
| `--direction` | `spot-to-perp` or `perp-to-spot` | Transfer direction |

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--asset` | `USDC` | `USDC` | Transfer asset (only USDC allowed) |

### Output

```json
{"ok": true, "data": {"amount": "100", "direction": "spot-to-perp", "status": "submitted"}}
```
<!-- shape from CLI flag metadata; not a captured run -->

### Confirm before executing

Show ALL of: amount, direction, venue. Do not run until the user approves.

### Examples

```bash
mm perps transfer --venue hyperliquid --amount 100 --direction spot-to-perp --yes --toon
```

## Errors

| Code | Cause | Recovery |
| --- | --- | --- |
| `ValidationError` | Malformed flag value, unknown symbol, `--limit-px` missing with `--type limit`, or both/neither of `--symbol`/`--all` on close | Re-check values against the tables above; list markets with `mm perps markets --venue hyperliquid --toon` |
| Insufficient margin / balance | Venue account cannot cover the notional at the requested size | `mm perps balance --venue hyperliquid --toon`; offer `mm perps deposit` or a smaller size, after user approval |
| Leverage above market max | `--leverage` exceeds the market's `maxLeverage` | Read `maxLeverage` from `mm perps markets --symbol <symbol>` and re-quote |
| Order or position not found | Wrong `<order-id>`, or no open position for `<symbol>` | Re-list with `mm perps orders` / `mm perps positions` |
| `NOT_INITIALIZED` | Project has no wallet mode | Follow workflows/onboarding.md, then retry |

Full code list: references/errors.md.
