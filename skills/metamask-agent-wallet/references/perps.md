# Perpetual Trading Commands

Use `perps` commands to trade perpetual futures on supported venues. Currently supported venue: `hyperliquid`.

## Common Flags

All `perps` commands accept these flags:

| Name | Required | Description |
| --- | --- | --- |
| `--venue` | Yes | Target perpetual venue: `hyperliquid` |
| `--network` | No | Target network: `mainnet` or `testnet`. Default is `mainnet` |

State-changing perps commands accept `--yes` to skip interactive confirmation. Perps commands do not use `--wait`.

## `perps markets` Command

List perpetual markets for a venue.

### Syntax

```bash
mm-dev perps markets --venue <venue> [--network <network>] [--symbol <symbol>] [--symbols <list>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--venue` | Yes | Target perpetual venue |
| `--network` | No | Target network |
| `--symbol` | No | Filter to a single market symbol |
| `--symbols` | No | Filter to multiple comma-separated market symbols |

### Example

```bash
mm-dev perps markets --venue hyperliquid
mm-dev perps markets --venue hyperliquid --symbol BTC
mm-dev perps markets --venue hyperliquid --symbols BTC,ETH,SOL --network testnet
```

## `perps balance` Command

Show the connected wallet's perpetual account balances for a venue.

### Syntax

```bash
mm-dev perps balance --venue <venue> [--network <network>]
```

### Example

```bash
mm-dev perps balance --venue hyperliquid
mm-dev perps balance --venue hyperliquid --network testnet
```

## `perps positions` Command

List open positions for the connected wallet on a venue.

### Syntax

```bash
mm-dev perps positions --venue <venue> [--network <network>]
```

### Example

```bash
mm-dev perps positions --venue hyperliquid
mm-dev perps positions --venue hyperliquid --network testnet
```

## `perps quote` Command

Estimate entry price, notional, fees, and liquidation price without placing an order.

### Syntax

```bash
mm-dev perps quote --venue <venue> --symbol <symbol> --side <side> --size <size> --leverage <leverage> [--type <type>] [--limit-px <price>] [--network <network>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--venue` | Yes | Target perpetual venue |
| `--symbol` | Yes | Market symbol, such as `BTC` |
| `--side` | Yes | Position direction: `long` or `short` |
| `--size` | Yes | Size in base asset |
| `--leverage` | Yes | Desired leverage |
| `--type` | No | Order type: `market` or `limit`. Default is `market` |
| `--limit-px` | If `--type limit` | Limit price |
| `--network` | No | Target network |

### Example

```bash
mm-dev perps quote --venue hyperliquid --symbol BTC --side long --size 0.01 --leverage 5
mm-dev perps quote --venue hyperliquid --symbol ETH --side short --size 1 --leverage 10 --type limit --limit-px 2500
```

## `perps open` Command

Open a new perpetual position by placing an order.

### Syntax

```bash
mm-dev perps open --venue <venue> --symbol <symbol> --side <side> --size <size> --leverage <leverage> [--type <type>] [--limit-px <price>] [--max-slippage-bps <bps>] [--network <network>] [--dry-run] [--yes]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--venue` | Yes | Target perpetual venue |
| `--symbol` | Yes | Market symbol |
| `--side` | Yes | Position direction: `long` or `short` |
| `--size` | Yes | Size in base asset |
| `--leverage` | Yes | Desired leverage |
| `--type` | No | Order type: `market` or `limit`. Default is `market` |
| `--limit-px` | If `--type limit` | Limit price |
| `--max-slippage-bps` | No | Slippage cap in basis points for IOC market pricing |
| `--network` | No | Target network |
| `--dry-run` | No | Validate and preview without signing or submitting |
| `--yes` | No | Skip interactive confirmation |

### Example

```bash
mm-dev perps open --venue hyperliquid --symbol BTC --side long --size 0.01 --leverage 5
mm-dev perps open --venue hyperliquid --symbol ETH --side short --size 1 --leverage 10 --type limit --limit-px 2500
mm-dev perps open --venue hyperliquid --symbol BTC --side long --size 0.05 --leverage 3 --dry-run
```

## `perps orders` Command

List resting orders for the connected wallet on a venue.

### Syntax

```bash
mm-dev perps orders --venue <venue> [--network <network>]
```

### Example

```bash
mm-dev perps orders --venue hyperliquid
mm-dev perps orders --venue hyperliquid --network testnet
```

## `perps close` Command

Close one position, part of a position, or all open positions.

### Syntax

```bash
mm-dev perps close --venue <venue> [--symbol <symbol>] [--size <size>] [--all] [--max-slippage-bps <bps>] [--network <network>] [--dry-run] [--yes]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--venue` | Yes | Target perpetual venue |
| `--symbol` | Yes, unless `--all` | Market symbol to close |
| `--size` | No | Partial close size; omit for full close |
| `--all` | No | Close every open position; mutually exclusive with `--symbol` |
| `--max-slippage-bps` | No | Slippage cap in basis points for IOC pricing |
| `--network` | No | Target network |
| `--dry-run` | No | Validate and preview without signing or submitting |
| `--yes` | No | Skip interactive confirmation |

### Example

```bash
mm-dev perps close --venue hyperliquid --symbol BTC
mm-dev perps close --venue hyperliquid --symbol ETH --size 0.5
mm-dev perps close --venue hyperliquid --all
mm-dev perps close --venue hyperliquid --symbol BTC --dry-run
```

## `perps modify` Command

Modify leverage, take-profit, or stop-loss for an existing position.

### Syntax

```bash
mm-dev perps modify --venue <venue> --symbol <symbol> [--leverage <leverage>] [--tp <price>] [--sl <price>] [--network <network>] [--dry-run] [--yes]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--venue` | Yes | Target perpetual venue |
| `--symbol` | Yes | Market symbol |
| `--leverage` | No | New leverage value |
| `--tp` | No | Take-profit trigger price |
| `--sl` | No | Stop-loss trigger price |
| `--network` | No | Target network |
| `--dry-run` | No | Validate and preview without signing or submitting |
| `--yes` | No | Skip interactive confirmation |

### Validation Rules

- At least one of `--leverage`, `--tp`, or `--sl` must be provided.

### Example

```bash
mm-dev perps modify --venue hyperliquid --symbol BTC --leverage 10
mm-dev perps modify --venue hyperliquid --symbol ETH --tp 3000 --sl 2000
mm-dev perps modify --venue hyperliquid --symbol BTC --leverage 3 --dry-run
```

## `perps cancel` Command

Cancel a resting perps order.

### Syntax

```bash
mm-dev perps cancel --venue <venue> --order-id <id> [--network <network>] [--yes]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--venue` | Yes | Target perpetual venue |
| `--order-id` | Yes | Order ID to cancel |
| `--network` | No | Target network |
| `--yes` | No | Skip interactive confirmation |

### Example

```bash
mm-dev perps cancel --venue hyperliquid --order-id 12345
mm-dev perps cancel --venue hyperliquid --order-id 12345 --yes
```

## `perps deposit` Command

Deposit USDC into a perpetual venue.

### Syntax

```bash
mm-dev perps deposit --venue <venue> --amount <amount> [--asset <asset>] [--source-chain <chain>] [--network <network>] [--yes]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--venue` | Yes | Target perpetual venue |
| `--amount` | Yes | Amount to deposit |
| `--asset` | No | Asset to deposit; typically `USDC` |
| `--source-chain` | No | Source chain for deposit |
| `--network` | No | Target network |
| `--yes` | No | Skip interactive confirmation |

### Example

```bash
mm-dev perps deposit --venue hyperliquid --amount 100 --asset USDC
mm-dev perps deposit --venue hyperliquid --amount 100 --asset USDC --yes
```

## `perps withdraw` Command

Withdraw USDC from a perpetual venue.

### Syntax

```bash
mm-dev perps withdraw --venue <venue> --amount <amount> [--asset <asset>] [--destination <address>] [--network <network>] [--yes]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--venue` | Yes | Target perpetual venue |
| `--amount` | Yes | Amount to withdraw |
| `--asset` | No | Asset to withdraw; typically `USDC` |
| `--destination` | No | Destination address; defaults to the connected wallet |
| `--network` | No | Target network |
| `--yes` | No | Skip interactive confirmation |

### Example

```bash
mm-dev perps withdraw --venue hyperliquid --amount 50 --asset USDC
mm-dev perps withdraw --venue hyperliquid --amount 50 --asset USDC --destination 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18 --yes
```
