# mm chains

Discover the blockchain networks the CLI supports and their chain IDs.

## Prerequisites

- `mm doctor` reports `authenticated: true` and `initialized: true` (SKILL.md § Preflight).
- Only the `eip155` (EVM) namespace is currently listed: Ethereum, Polygon, BSC, Avalanche,
  Optimism, Celo, Arbitrum, Base, Linea, plus their common testnets.

## mm chains list

List all supported blockchain networks across all namespaces. Read-only. No flags beyond
global flags.

### Syntax

```bash
mm chains list
```

Global flags apply — see SKILL.md § Global flags.

### Output

```
ok: true
data:
  chains[17]{key,chainNamespace,caip2,chainId,name,selected}:
    ethereum,eip155,"eip155:1",1,Ethereum,false
    polygon,eip155,"eip155:137",137,Polygon,false
    bsc,eip155,"eip155:56",56,Binance Smart Chain (BSC),false
    avalanche,eip155,"eip155:43114",43114,Avalanche,false
    optimism,eip155,"eip155:10",10,Optimism,false
    arbitrum,eip155,"eip155:42161",42161,Arbitrum One,false
    base,eip155,"eip155:8453",8453,Base,false
    linea,eip155,"eip155:59144",59144,Linea,false
    sepolia,eip155,"eip155:11155111",11155111,Sepolia Test Network,false
    arbitrum-sepolia,eip155,"eip155:421614",421614,Arbitrum Sepolia,false
    base-sepolia,eip155,"eip155:84532",84532,Base Sepolia,false
```

Capture: `chainId` → use as `<chain-id>`; `caip2` → use as `<caip2>` in other commands.

### Examples

```bash
mm chains list --toon
```

## Errors

| Code | Cause | Recovery |
| --- | --- | --- |
| `NETWORK_UNREACHABLE` | No network connectivity | Check the connection, retry |
| `NOT_INITIALIZED` | Project has no wallet mode | Follow workflows/onboarding.md, then retry |

Full code list: references/errors.md.
