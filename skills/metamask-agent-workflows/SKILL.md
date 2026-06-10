---
name: metamask-agent-workflows
description: Use when the user needs to perform multi-step operations with the MetaMask Agentic CLI such as onboarding, login, swapping tokens, bridging across chains, opening/closing/modifying perpetual positions, prediction market trading, Aave V3 lending and borrowing, or troubleshooting CLI issues.
license: MIT
metadata:
  author: metamask
  version: "2.1.0"
  cliVersion: "1.0.0"
---

# MetaMask Agent Workflows

Repeatable multi-step patterns for the `mm` CLI. Load a workflow file when the user's request is a pattern, not a single command.

## Workflow Routing

| Pattern | Workflow |
| --- | --- |
| First time setup and onboarding | [onboarding.md](workflows/onboarding.md) |
| Login flow | [login.md](workflows/login.md) |
| Troubleshooting decision tree | [troubleshooting.md](workflows/troubleshooting.md) |
| Swap quote-review-execute flow | [swap.md](workflows/swap.md) |
| Bridge quote-review-execute flow | [bridge.md](workflows/bridge.md) |
| Open a perpetual position flow | [perps-open-position.md](workflows/perps-open-position.md) |
| Close a perpetual position flow | [perps-close-position.md](workflows/perps-close-position.md) |
| Modify a perpetual position flow | [perps-modify-position.md](workflows/perps-modify-position.md) |
| Predict first-time setup and credentials | [predict-setup.md](workflows/predict-setup.md) |
| Deposit or withdraw pUSD from Predict wallet | [predict-funding.md](workflows/predict-funding.md) |
| Search and browse prediction markets | [predict-markets.md](workflows/predict-markets.md) |
| Quote and place a prediction order | [predict-place-order.md](workflows/predict-place-order.md) |
| View or cancel Predict orders and positions | [predict-manage-orders.md](workflows/predict-manage-orders.md) |
| View Predict portfolio and redeem winnings | [predict-portfolio.md](workflows/predict-portfolio.md) |
| Token discovery, prices, and market data | [market-data.md](workflows/market-data.md) |
| Supply assets to Aave V3 | [aave-supply.md](workflows/aave-supply.md) |
| Withdraw assets from Aave V3 | [aave-withdraw.md](workflows/aave-withdraw.md) |
| Borrow from Aave V3 | [aave-borrow.md](workflows/aave-borrow.md) |
| Repay Aave V3 debt | [aave-repay.md](workflows/aave-repay.md) |
| Toggle Aave V3 collateral | [aave-collateral.md](workflows/aave-collateral.md) |
| Check Aave V3 positions and health factor | [aave-positions.md](workflows/aave-positions.md) |
| Discover Aave V3 tokens, rates, and liquidity | [aave-markets.md](workflows/aave-markets.md) |

Always use `--toon` for command output unless the user explicitly requests a different format.

## Preflight

Run these checks before the first CLI operation in a session, in order.

### 1. Version compatibility

This skill is written for `@metamask/agentic-cli` **v1.0.0** (see `cliVersion` in the frontmatter). Check the installed version:

```bash
mm --version
```

The installed version is the value after `@metamask/agentic-cli/` (e.g. `@metamask/agentic-cli/1.0.0 darwin-arm64 node-v24.14.1`). Compare its `major.minor` against the pinned `cliVersion`. Optionally check the latest published version (best-effort; skip silently on network failure):

```bash
npm view @metamask/agentic-cli version
```

If the installed `major.minor` differs from the pinned `cliVersion`, or the installed version is behind the latest release, warn the user once and continue:

> Version mismatch: installed CLI `<installed>`, this skill is pinned to `1.0.0`, latest release is `<latest>`. Command syntax in this skill may be inaccurate until they are aligned. Update the CLI with `npm install -g @metamask/agentic-cli@latest`, then re-install the skills with `npx skills add metaMask/agent-skills`.

Run this check once per session. Do not block operations on it.

### 2. Authentication

```bash
mm auth status
```

If the user is not authenticated, follow `workflows/onboarding.md` for first time setup, or `workflows/login.md` for login.

## Command Discovery

Before constructing any command, run `mm <command> --help` to confirm the exact flags, syntax, and defaults. Do not guess flags from memory.

## Output Rules

- Route silently. Do not announce which workflow you are loading.
- Surface errors from commands verbatim. Do not mask or reword them.
- If a command fails, check `mm <command> --help` and guide from there.
