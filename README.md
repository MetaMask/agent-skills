# MetaMask Agent CLI Skills

SKILLs for the MetaMask Agent CLI (`@metamask/agentic-cli` v1.0.0). These skills enable AI agents to authenticate, manage wallets, swap tokens, bridge across chains, trade perpetual futures, and more using the MetaMask Agent CLI.

## Skills

| Skill | Description |
| --- | --- |
| [`metamask-agent-wallet`](./skills/metamask-agent-wallet/SKILL.md) | Full CLI reference skill that routes the agent to topic-specific reference docs for all MetaMask Agent CLI commands — auth, wallets, transfers, signing, swaps, bridges, perps, prediction markets, market data, and calldata decoding. |
| [`metamask-agent-workflows`](./skills/metamask-agent-workflows/SKILL.md) | Multistep workflow templates for complex operations like onboarding, swaps, bridges, and perps trading. It doesn't include reference docs — relies on `--help` for command details instead. |

## Installation

Install with [Vercel's Skills CLI](https://skills.sh):

```bash
npx skills add metaMask/agent-skills
```

Select any one of the SKILLs upon prompt. 