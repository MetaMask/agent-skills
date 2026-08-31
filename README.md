# MetaMask Agent CLI Skills

SKILLs for the MetaMask Agent CLI (`@metamask/agent-wallet` v6.1.5). These skills enable AI agents to authenticate, manage wallets, swap tokens, bridge across chains, trade perpetual futures, earn yield on DeFi vaults, and more using the MetaMask Agent CLI.

Works with **Cursor**, **Claude Code**, and the [Vercel Skills CLI](https://skills.sh).

## Skills

| Skill | Description |
| --- | --- |
| [`metamask-agent-wallet`](./skills/metamask-agent-wallet/SKILL.md) | Full CLI skill that routes the agent to topic-specific reference docs (`references/`) for all MetaMask Agent CLI commands — auth, wallets, transfers, signing, swaps, bridges, perps, prediction markets, DeFi earn/yield vaults, market data, x402 payments, and calldata decoding — plus multistep workflow templates (`workflows/`) for onboarding, swaps, bridges, perps, prediction markets, and earn. |

## Installation

### Skills CLI

```bash
npx skills add metaMask/agent-skills
```

### Cursor

1. Clone or open this repository in Cursor (or copy it into your Cursor plugins directory).
2. Cursor detects `.cursor-plugin/plugin.json` and loads skills from `skills/`.

### Claude Code

Load the plugin from a local checkout:

```bash
claude --plugin-dir /path/to/agent-skills
```

Claude Code detects `.claude-plugin/plugin.json` and loads skills from `skills/`.
