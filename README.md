# MetaMask Agent CLI Skills

SKILLs for the MetaMask Agent CLI (`@metamask/agentic-cli` v4.0.1). These skills enable AI agents to authenticate, manage wallets, swap tokens, bridge across chains, trade perpetual futures, and more using the MetaMask Agent CLI.

## Skills

| Skill | Description |
| --- | --- |
| [`metamask-agent-wallet`](./skills/metamask-agent-wallet/SKILL.md) | Full CLI skill that routes the agent to topic-specific reference docs (`references/`) for all MetaMask Agent CLI commands — auth, wallets, transfers, signing, swaps, bridges, perps, prediction markets, Aave V3, market data, x402 payments, and calldata decoding — plus multistep workflow templates (`workflows/`) for onboarding, swaps, bridges, perps, prediction markets, and Aave. Every doc follows a fixed template (one canonical syntax per command, flag tables verified against `mm --help`, captured outputs, confirmation checklists) so that even small models can execute commands by string substitution. Runtime helper scripts: `amount_to_hex.py`, `encode_approve.py`, `x402_pay.py`. |

## Installation

Install with [Vercel's Skills CLI](https://skills.sh):

```bash
npx skills add metamask/agent-skills
```

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for skill updates and how to catch up from an older version.