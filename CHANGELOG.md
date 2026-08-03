# Changelog

All notable changes to the MetaMask Agent CLI Skills are documented here.

These skills track the [`@metamask/agentic-cli`](https://github.com/MetaMask/agentic) releases.
Each entry lists the skill `version` (frontmatter) and the CLI `cliVersion` it targets,
along with the user-facing CLI changes that motivated the skill update. Use this log to
catch up if you are on an older skill version — apply the entries above yours in order.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and the skills follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [6.3.0] — targets CLI v5.3.0

### Added

- `mm predict history` command: list deposit-wallet activity (trades by default, or `--type redeem` for past redemptions). Supports pagination (`--limit`, `--offset`), time range (`--start`, `--end`), sorting (`--sort-by`, `--sort-direction`), and side filtering (`--side`). Each trade row includes settlement `result` (`won`, `lost`, `pending`), `redeemed` flag, and `amountWon` payout.
- `mm predict history get <condition-id>` command: show trade/redeem history for a specific market condition.
- New workflow: `workflows/predict-history.md` for browsing and filtering predict trade/redeem history.
- New error codes: `INVALID_EVM_ADDRESS` (invalid transfer recipient), `RELAY_TIMEOUT` (gasless relay poll timeout with recovery hint), `TX_REVERTED` (on-chain RPC revert with `failure_reason`), `RATE_LIMITED` (venue rate limit, e.g. Hyperliquid HTTP 429), `INVALID_AMOUNT` (non-positive/malformed amount on transfers).
- `ALREADY_LOGGED_OUT` reason on `mm logout` when no active session exists (exit 0, not an error).
- `mm tx history` output enriched with `chainName`, `chainId`, `explorerUrl`, and `protocol` metadata fields.

### Changed

- Swap MFA timeouts now return `RELAY_TIMEOUT` (gasless relay) or `JOB_TIMEOUT` (sequential legs) instead of generic `SWAP_ERROR`, with recovery hint to check `mm wallet requests watch --polling-id <id>`.
- Gasless relay polling now respects `--wallet-timeout` (default 10 minutes) instead of the fox-sdk ~5-minute default.
- Perps HTTP 429 errors from Hyperliquid now map to `RATE_LIMITED` instead of `HYPERLIQUID_ERROR`.
- Token and route discovery errors (`TOKEN_NOT_FOUND`, `TOKEN_NO_ADDRESS`, `TOKEN_NOT_SUPPORTED`, `NATIVE_ASSET_UNSUPPORTED`, `INVALID_GAS_TOKEN`, `NO_QUOTES`) now suggest `mm token list search` in recovery hints.
- Earn wallet approval intents now use human-readable amounts and token symbols (e.g. "Supply 0.998 USDC to Fluid") instead of base units and contract addresses.
- `mm login qr` aborts promptly with `MWP_CANCELLED` when MetaMask Mobile cancels dashboard authorization, instead of hanging until timeout.
- `mm wallet balance` tolerates missing `nativeCurrency` metadata (falls back to built-in metadata or ETH/18).
- Bumped `cliVersion` to `5.3.0`.

## [6.2.1] — targets CLI v5.2.1

### Added

- New predict error codes: `PREDICT_ORDER_SIZE_TOO_SMALL` (order size below exchange minimum), `PREDICT_ORDER_NOT_FILLED` (FOK order could not be fully filled). These are classified from unstructured CLOB place rejections.
- New predict error codes with actionable hints: `PREDICT_REDEEM_NONE`, `PREDICT_REDEEM_NOT_FOUND`, `PREDICT_REDEEM_MISSING_TARGET`.
- `mm tx --hash <hash>` command: look up a transaction by hash. Added to SKILL.md routing table and `references/tx-history.md`.

### Changed

- All expected predict error codes now return actionable, per-code hints instead of a generic "Re-check inputs and mode" fallback. Affected codes include `PREDICT_SETUP_REQUIRED`, `PREDICT_AUTH_REQUIRED`, `PREDICT_AUTH_INVALID`, `PREDICT_INSUFFICIENT_BALANCE`, `PREDICT_INSUFFICIENT_FUNDING_BALANCE`, `PREDICT_INSUFFICIENT_ALLOWANCE`, `PREDICT_CANCEL_TARGET_REQUIRED`, and others.
- Bumped `cliVersion` to `5.2.1`.

## [6.2.0] — targets CLI v5.2.0

### Added

- `--tick-size` flag on `mm predict quote` and `mm predict place` to override the market tick size. Supported values: `0.1`, `0.01`, `0.001`, `0.0001`. Defaults to the CLOB tick for the token.
- Swap quote soft-unavailable outcomes: `mm swap quote` now returns a soft `{ kind: "unavailable", reason, message, hint }` envelope (exit 0) when the bridge returns zero routes for actionable reasons (`NO_QUOTES`, `AMOUNT_TOO_LOW`, `AMOUNT_TOO_HIGH`, `SLIPPAGE_TOO_HIGH`, `SLIPPAGE_TOO_LOW`, `TOKEN_NOT_SUPPORTED`, `RWA_GEO_RESTRICTED`, `RWA_NATIVE_TOKEN_UNSUPPORTED`, `RWA_MARKET_UNAVAILABLE`). Only `QUOTE_RETRY` remains a hard error.
- New error codes: `WALLET_NOT_REGISTERED` (BYOK init registration failure), `QUOTE_RETRY` (transient bridge retry signal), `PREDICT_INSUFFICIENT_GAS` (POL gas shortfall on Polygon deposits).
- `--tick-size` validation rule added to SKILL.md input validation table.

### Changed

- `mm init --wallet byok` now requires server-side wallet registration to succeed. Failure throws `WALLET_NOT_REGISTERED` and rolls back the wallet mode.
- Predict deposit gas errors now surface as `PREDICT_INSUFFICIENT_GAS` with a POL-specific hint instead of collapsing to generic `PREDICT_ERROR`.
- Transfer MFA intents show token symbol instead of contract address; swap/bridge intents include approximate destination amount.
- Bumped `cliVersion` to `5.2.0`.

## [6.1.0] — targets CLI v5.1.0

### Added

- `--wait` flag on `mm earn supply` to poll and confirm the position is reflected after deposit.
- New error codes: `JOB_TIMEOUT`, `REQUEST_NOT_FOUND`, `TX_DENIED`, `TX_EXPIRED`, `TX_FAILED`.
- New troubleshooting rows for `JOB_TIMEOUT`, `TX_DENIED`, `TX_EXPIRED`, `AUTH_FAILED` after session expiry.

### Changed

- Default wallet job poll timeout raised from 5 minutes to 10 minutes.
- Perps deposit/withdraw/order errors now show actionable hints with minimum amounts.
- Auth failures during operations now consistently produce `AUTH_FAILED` with login guidance.
- Bumped `cliVersion` to `5.1.0`.

## [6.0.0] — targets CLI v5.0.1

### Changed

- `mm doctor` no longer checks for the removed `metamask-agent-workflows` skill. Only `metamask-agent-wallet` is checked.
- Bumped `cliVersion` to `5.0.1`.

## [6.0.0] — targets CLI v5.0.0

### Added

- Earn commands: `mm earn markets`, `mm earn positions`, `mm earn supply`, `mm earn withdraw` for DeFi yield vaults via LiFi. New reference (`references/earn.md`) and workflows (`workflows/earn-supply.md`, `workflows/earn-withdraw.md`). Earn error codes added to `references/errors.md`.
- ERC-7821 batch execution: on eligible chains and accounts, the CLI batches approval + trade into a single transaction. Documented in swap and bridge workflows.
- Intelligent quote selection: the CLI skips quotes the wallet cannot cover gas for and prefers gasless (EIP-7702) quotes when native balance is low. New `INSUFFICIENT_GAS` error code.
- New swap/bridge error codes: `INSUFFICIENT_GAS`, `REFUEL_UNSUPPORTED_ROUTE`, `AMOUNT_TOO_LOW`, `AMOUNT_TOO_HIGH`, `SLIPPAGE_TOO_HIGH`, `SLIPPAGE_TOO_LOW`, `TOKEN_NOT_SUPPORTED`, `RWA_GEO_RESTRICTED`, `RWA_NATIVE_TOKEN_UNSUPPORTED`, `RWA_MARKET_UNAVAILABLE`.
- New validation error codes: `UNKNOWN_FLAG`, `MISSING_ARG`, `UNEXPECTED_ARG`, `UNSUPPORTED_CHAIN`.
- `--strategy` flag on `mm swap execute` (re-quote mode).
- `--otp-pair` flag on `mm login browser` to restore the legacy MWP 6-digit pairing-code flow.
- `INSUFFICIENT_FUNDS` error in swap execute path with pre-execute balance check.
- Transaction notification guidance for QR login users in troubleshooting workflow (`AWAITING_MFA` row).

### Changed

- `mm login browser` default changed from MWP pairing to paste-token flow. The user pastes a `cliToken:cliRefreshToken` from the dashboard.
- Swap and bridge workflows now default to `--all-quotes` to show all available routes.
- Quote presentation: when showing multiple quotes, show a summary comparison table, then full details for the recommended quote. Show full details for any user-selected route before executing.
- `--all-quotes` and `--yes` cannot be used together (`INVALID_SWAP_PARAMS`).
- Removed bold formatting from all skill files.
- Removed interactive TTY section from `references/swap.md` (not relevant for agents).

### Removed

- Aave V3 workflow files (`aave-borrow.md`, `aave-collateral.md`, `aave-markets.md`, `aave-positions.md`, `aave-repay.md`, `aave-supply.md`, `aave-withdraw.md`). Replaced by the generic earn commands which support Aave and other protocols.

## [5.0.1] — targets CLI v4.0.1

### Removed

- **`metamask-agent-workflows` skill.** Its workflow templates were a subset of the
  `metamask-agent-wallet` skill's `workflows/` directory (the wallet copies were also more
  up-to-date). The repo now ships a single `metamask-agent-wallet` skill that bundles both the
  reference docs and the workflow templates. Install it with
  `npx skills add metaMask/agent-skills`.

### Changed

- `references/doctor.md`: document that `mm doctor` now detects **project-local** MetaMask AI
  skills when the global skill lock file (`~/.agents/.skill-lock.json`) exists but lacks
  MetaMask entries. ([agentic#263](https://github.com/MetaMask/agentic/pull/263))
- Bumped `cliVersion` to `4.0.1` across both skills and updated README.

### Notes

- CLI v4.0.1 also improved Sentry error reporting and surfaced reportable failures in
  Segment analytics ([agentic#264](https://github.com/MetaMask/agentic/pull/264)); these are
  internal telemetry changes with no impact on the command surface, so no skill docs changed.

## [5.0.0] — targets CLI v4.0.0

### Added

- BYOK (bring-your-own-key) parity for `mm init` and `mm wallet create`: persisted BYOK
  wallets are registered server-side, prompt for a trading mode, and apply the server trading
  policy — matching the server-wallet flow. ([agentic#246](https://github.com/MetaMask/agentic/pull/246))

### Fixed

- `mm predict` deposit-wallet setup no longer stalls with contradictory relayer errors when a
  cached address was derived as legacy UUPS instead of BeaconProxy.
  ([agentic#259](https://github.com/MetaMask/agentic/pull/259))

## Earlier CLI history

For CLI releases prior to v4.0.0, see the upstream
[`packages/agentic-cli/CHANGELOG.md`](https://github.com/MetaMask/agentic/blob/main/packages/agentic-cli/CHANGELOG.md).
Highlights that shaped the current skill surface:

- **v3.2.0** — confirmation prompts (with `--yes`) before `mm logout` / `mm reset`; npm update
  notifier; `mm wallet list` refreshes the remote roster before listing.
- **v3.0.0** — **breaking:** `mm login google` / `mm login email` removed; use
  `mm login browser` (Google or email via the MetaMask dashboard). Bridge `--refuel` added;
  deposit preflight checks; auto-rehydrate on login.
- **v2.0.0** — **breaking:** wallet policy moved to `mm wallet policy get|set|template`
  (`mm wallet show` / `create` return `policyYaml` instead of `policies`). Added `mm doctor`,
  `mm transaction` history, and major CLI startup performance work.
- **v1.0.0** — `mm wallet add-fund` (QR funding), trading-mode get/set commands, and
  `mm swap`/`mm predict` recipient support.
