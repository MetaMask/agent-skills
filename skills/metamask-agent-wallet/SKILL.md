---
name: metamask-agent-wallet
description: Use when the user asks anything about blockchain wallets, transactions, signing, token transfers, supported chains, wallet balances, perpetual futures trading, prediction markets, token swaps, cross-chain bridges, market data, token discovery, decoding EVM calldata, Aave V3 lending and borrowing, or authentication via the MetaMask Agentic CLI; also when an HTTP request returns 402 Payment Required (x402) or the agent needs to pay for a paywalled API, endpoint, file, or resource over HTTP. Single entry point for all mm CLI operations.
license: MIT
metadata:
  author: metamask
  version: "6.0.0"
  cliVersion: "4.0.1"
---

# MetaMask Agentic CLI Skill

This skill documents the `mm` CLI. The loop for every request is:
**route → read the reference → validate inputs → confirm with the user → execute**.

## How to use this skill

1. Match the user's intent to a row in the Command Routing table below.
2. Read the listed reference file BEFORE constructing any command.
3. If the request is a multi-step pattern (a row in the Workflows table), read that workflow too.
4. Build the command by replacing placeholders per the legend below. Change nothing else.
5. For state-changing commands, show the user the fields listed in the reference's
   "Confirm before executing" section and wait for approval, then execute with `--toon`.

## Placeholder legend

In syntax lines, `<angle-bracket>` tokens are placeholders: replace the whole token, brackets
included, with a real value. Everything else is literal. Never copy a value that contains `...`
or `…`. Addresses are always the full `0x` + 40 hex characters.

| Placeholder | Format | Example |
| --- | --- | --- |
| `<address>` | `^0x[0-9a-fA-F]{40}$` | `0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48` |
| `<amount>`, `<size>` | positive decimal `^\d+\.?\d*$` | `0.5` |
| `<chain-id>` | positive integer | `1` (Ethereum), `137` (Polygon) |
| `<caip2>` | `eip155:<chain-id>` | `eip155:1` |
| `<caip19>` | see references/concepts.md | `eip155:1/erc20:0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48` |
| `<token>` | symbol or `<address>` | `ETH`, `USDC` |
| `<symbol>` | market symbol | `BTC` |
| `<quote-id>` | string from `mm swap quote` output | — |
| `<polling-id>` | string from a state-changing command's output | — |
| `<token-id>` | Predict outcome token ID string | — |
| `<order-id>` | Predict/perps order ID | — |
| `<condition-id>` | Predict market condition ID (`0x` + 64 hex) | — |
| `<payload-json>` | valid JSON, single-quoted in shell | `'{"to":"0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48","value":"0x0","data":"0x095ea7b3"}'` |
| `<calldata>`, `<hex>` | `^0x[0-9a-fA-F]+$` | — |
| `<tx-hash>` | `^0x[0-9a-fA-F]{64}$` | — |
| `<url>` | `https://` URL | — |
| `<unix>` | Unix timestamp in seconds (`date +%s`) | `1783600000` |
| `<venue>` | perps venue | `hyperliquid` |
| `<network>` | `mainnet` or `testnet` | `mainnet` |
| `<side>` | perps: `long`/`short`; predict: `buy`/`sell` | `long` |
| `<price>`, `<limit-price>` | positive decimal; predict prices in `(0, 1]` | `0.65` |
| `<order-type>` | predict: `GTC`, `GTD`, `FOK`, `FAK` | `GTC` |
| `<query>` | free-text search string | `bitcoin` |
| `<slug>` | URL-style identifier from a listing | — |
| `<cursor>` | pagination cursor from a previous response | — |
| `<pool-address>` | Aave pool contract, `^0x[0-9a-fA-F]{40}$` | — |

A reference may define additional placeholders where it uses them; the same rules apply.

## Global flags

Valid on every command. They are deliberately NOT repeated in reference flag tables.

| Flag | Short | Description |
| --- | --- | --- |
| `--format` | `-f` | Output format: `text`, `json`, or `toon` (default: `text` in TTY, `json` when piped) |
| `--json` | | Shorthand for `--format=json` |
| `--toon` | | Shorthand for `--format=toon` |
| `--verbose` | `-v` | Debug logs on stderr, for troubleshooting |

Always use `--toon` unless the user explicitly requests another format. Commands that create
wallet jobs also accept `--wallet-timeout <seconds>` (max 600) — see references/concepts.md.

## Preflight (run once per session, before the first mm command)

1. Run `mm --version`. If the `major.minor` (first two numbers) differs from `cliVersion` in
   this file's frontmatter, warn once: "Version mismatch: installed `<installed>`, skill pinned
   to `4.0.1`. Update with `npm install -g @metamask/agentic-cli@latest`, then re-install skills
   with `npx skills add metamask/agent-skills`." Then continue.
2. Run `mm doctor`. Real output shape:

```json
{
  "ok": true,
  "data": {
    "cli": "4.0.1",
    "env": "prod",
    "authenticated": true,
    "initialized": true,
    "hints": []
  }
}
```

3. If `authenticated` is `false` → follow workflows/login.md.
4. If `initialized` is `false` → follow workflows/onboarding.md.
5. Re-run `mm doctor` after remediation. Do not run any other command until both are `true`.
6. Never use `mm init show` as the readiness check — it throws `NOT_INITIALIZED` on an
   uninitialized project instead of reporting state.

## Safety invariants

These apply to every operation.

1. **Secrets.** Never store, log, or display private keys, mnemonics, passwords, or auth
   tokens. Secrets travel only via the `MM_PASSWORD` / `MM_MNEMONIC` environment variables —
   never as `--password` or `--mnemonic` flags (references/concepts.md).
2. **Confirmation.** Before any state-changing command, show the user the exact fields listed
   in that command's "Confirm before executing" section and wait for explicit approval.

| Operation class | Rule |
| --- | --- |
| On-chain writes (transfer, send-transaction, swap/bridge execute, perps orders and fund moves, predict orders/deposit/withdraw/redeem, x402 pay, Aave) | Confirm the reference's field list first |
| Signing (sign-message, sign-typed-data) | Show the exact message/domain summary first |
| Cancel-all / redeem-all / `mm reset` | Confirm the exact destructive scope first |
| Read-only queries, auth, wallet management | No confirmation needed |

3. **Input hygiene.** Validate every user-provided value against the placeholder legend and the
   reference's "Value format" column. Reject values containing shell metacharacters
   (`; | & $ \` >`). Wrap JSON payloads in single quotes.
4. **Unfamiliar calldata.** If a payload was not constructed by you, run
   `mm decode --payload <calldata>` and confirm the decoded intent with the user before
   signing or sending. Apply the suspicious-payload checklist in references/concepts.md.

## Command routing

Match intent → read the reference → construct the command.

| User intent | Command | Reference |
| --- | --- | --- |
| Check CLI + session health | `mm doctor` | [doctor.md](references/doctor.md) |
| Check authentication status | `mm auth status` | [auth.md](references/auth.md) |
| Sign in (browser: Google/email) | `mm login browser` | [auth.md](references/auth.md) |
| Sign in (QR with MetaMask Mobile) | `mm login qr` | [auth.md](references/auth.md) |
| Sign out | `mm logout` | [auth.md](references/auth.md) |
| Wipe the local CLI session | `mm reset` | [auth.md](references/auth.md) |
| Set up wallet mode + trading mode | `mm init` | [auth.md](references/auth.md) |
| Show current init settings | `mm init show` | [auth.md](references/auth.md) |
| Show / set CLI configuration | `mm config get` / `mm config set` | [auth.md](references/auth.md) |
| Set / change / remove BYOK password | `mm wallet password set\|change\|remove` | [auth.md](references/auth.md) |
| Create a wallet | `mm wallet create` | [wallet.md](references/wallet.md) |
| List wallets | `mm wallet list` | [wallet.md](references/wallet.md) |
| Switch active wallet | `mm wallet select` | [wallet.md](references/wallet.md) |
| Show wallet details | `mm wallet show` | [wallet.md](references/wallet.md) |
| Show active wallet address | `mm wallet address` | [wallet.md](references/wallet.md) |
| Check balances | `mm wallet balance` | [wallet.md](references/wallet.md) |
| Show funding QR + address | `mm wallet add-fund` | [wallet.md](references/wallet.md) |
| Show / set trading mode | `mm wallet trading-mode get\|set` | [wallet.md](references/wallet.md) |
| View / set / template wallet policy | `mm wallet policy get\|set\|template` | [wallet.md](references/wallet.md) |
| List pending wallet requests | `mm wallet requests list` | [wallet-requests.md](references/wallet-requests.md) |
| Watch a polling id | `mm wallet requests watch` | [wallet-requests.md](references/wallet-requests.md) |
| Sign a plaintext message | `mm wallet sign-message` | [signing.md](references/signing.md) |
| Sign EIP-712 typed data | `mm wallet sign-typed-data` | [signing.md](references/signing.md) |
| Send a raw EVM transaction | `mm wallet send-transaction` | [transaction.md](references/transaction.md) |
| Transfer native / ERC-20 tokens | `mm transfer` | [transfer.md](references/transfer.md) |
| List supported chains | `mm chains list` | [chains.md](references/chains.md) |
| Decode EVM calldata | `mm decode` | [decode.md](references/decode.md) |
| Look up a transaction by hash | `mm tx` | [tx-history.md](references/tx-history.md) |
| List recent transactions | `mm tx history` | [tx-history.md](references/tx-history.md) |
| Spot prices | `mm price spot` | [price.md](references/price.md) |
| Historical prices | `mm price history` | [price.md](references/price.md) |
| Supported price currencies / networks | `mm price currencies` / `mm price networks` | [price.md](references/price.md) |
| Token metadata by CAIP-19 | `mm token assets` | [token.md](references/token.md) |
| Popular / trending / top-gainer tokens | `mm token list popular\|trending\|top-gainer` | [token.md](references/token.md) |
| Search tokens by name or symbol | `mm token list search` | [token.md](references/token.md) |
| Token API networks | `mm token networks` | [token.md](references/token.md) |
| List perps venues / DEXs | `mm perps list-venues` / `mm perps dexs` | [perps.md](references/perps.md) |
| List perp markets | `mm perps markets` | [perps.md](references/perps.md) |
| Perps balance / positions / orders | `mm perps balance\|positions\|orders` | [perps.md](references/perps.md) |
| Quote a perp order | `mm perps quote` | [perps.md](references/perps.md) |
| Open / close / modify a position | `mm perps open\|close\|modify` | [perps.md](references/perps.md) |
| Cancel a perps order | `mm perps cancel` | [perps.md](references/perps.md) |
| Perps deposit / withdraw / transfer | `mm perps deposit\|withdraw\|transfer` | [perps.md](references/perps.md) |
| Predict mode / one-time setup | `mm predict mode` / `mm predict setup` | [predict-account.md](references/predict-account.md) |
| Predict credentials / approvals | `mm predict auth` / `mm predict approve` | [predict-account.md](references/predict-account.md) |
| Predict backend status / geoblock | `mm predict status` / `mm predict geoblock` | [predict-account.md](references/predict-account.md) |
| Predict wallet balance / deposit / withdraw | `mm predict balance\|deposit\|withdraw` | [predict-account.md](references/predict-account.md) |
| Browse / search prediction markets | `mm predict markets list\|search\|get` | [predict-data.md](references/predict-data.md) |
| Polymarket events / series / tags | `mm predict events\|series\|tags list\|get` | [predict-data.md](references/predict-data.md) |
| Fetch a Predict order book | `mm predict book` | [predict-data.md](references/predict-data.md) |
| Quote / place a prediction order | `mm predict quote` / `mm predict place` | [predict-trade.md](references/predict-trade.md) |
| Cancel prediction orders | `mm predict cancel` | [predict-trade.md](references/predict-trade.md) |
| Predict positions / orders / portfolio | `mm predict positions\|orders\|portfolio` | [predict-trade.md](references/predict-trade.md) |
| Redeem winning positions | `mm predict redeem` / `mm predict redeem list` | [predict-trade.md](references/predict-trade.md) |
| Watch a Predict job | `mm predict watch` | [predict-trade.md](references/predict-trade.md) |
| Get a swap or bridge quote | `mm swap quote` | [swap.md](references/swap.md) |
| Execute a swap or bridge | `mm swap execute` | [swap.md](references/swap.md) |
| Check swap / bridge status | `mm swap status` | [swap.md](references/swap.md) |
| Aave V3 lend / borrow / positions | `mm wallet send-transaction` + Aave API | [aave.md](references/aave.md) |
| Pay an HTTP 402 (x402) paywall | `python3 "$SKILL_DIR/scripts/x402_pay.py"` | [x402.md](references/x402.md) |
| Interpret a CLI error code | — | [errors.md](references/errors.md) |
| Term you don't recognize | — | [concepts.md](references/concepts.md) |

## Workflows

Load a workflow when the user's request is a multi-step pattern, not a single command.

| Pattern | Workflow |
| --- | --- |
| First-time setup and onboarding | [onboarding.md](workflows/onboarding.md) |
| Login flow | [login.md](workflows/login.md) |
| Troubleshooting decision tree | [troubleshooting.md](workflows/troubleshooting.md) |
| Same-chain swap (quote → confirm → execute) | [swap.md](workflows/swap.md) |
| Cross-chain bridge (quote → confirm → execute) | [bridge.md](workflows/bridge.md) |
| Open a perp position | [perps-open-position.md](workflows/perps-open-position.md) |
| Close a perp position | [perps-close-position.md](workflows/perps-close-position.md) |
| Modify a perp position | [perps-modify-position.md](workflows/perps-modify-position.md) |
| Predict first-time setup | [predict-setup.md](workflows/predict-setup.md) |
| Predict deposit / withdraw pUSD | [predict-funding.md](workflows/predict-funding.md) |
| Browse prediction markets | [predict-markets.md](workflows/predict-markets.md) |
| Quote and place a prediction order | [predict-place-order.md](workflows/predict-place-order.md) |
| View / cancel Predict orders and positions | [predict-manage-orders.md](workflows/predict-manage-orders.md) |
| Predict portfolio and redeem winnings | [predict-portfolio.md](workflows/predict-portfolio.md) |
| Token discovery, prices, market data | [market-data.md](workflows/market-data.md) |
| Supply assets to Aave V3 | [aave-supply.md](workflows/aave-supply.md) |
| Withdraw assets from Aave V3 | [aave-withdraw.md](workflows/aave-withdraw.md) |
| Borrow from Aave V3 | [aave-borrow.md](workflows/aave-borrow.md) |
| Repay Aave V3 debt | [aave-repay.md](workflows/aave-repay.md) |
| Toggle Aave V3 collateral | [aave-collateral.md](workflows/aave-collateral.md) |
| Aave V3 positions and health factor | [aave-positions.md](workflows/aave-positions.md) |
| Aave V3 markets, rates, liquidity | [aave-markets.md](workflows/aave-markets.md) |
| Pay an HTTP 402 (x402) request | [x402-pay.md](workflows/x402-pay.md) |

## Output rules

1. Route silently — do not announce which reference you are loading.
2. Surface CLI errors verbatim; do not mask or reword them.
3. If a command fails unexpectedly, run `mm <command> --help` and follow its `flags` list.
   Trust the `flags` descriptions over the `usage` string — some usage strings are inaccurate.
4. Async model (`pollingId`, `--wait`, `intent`): references/concepts.md.
