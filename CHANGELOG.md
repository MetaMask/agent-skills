# Changelog

All notable changes to the MetaMask Agent CLI Skills are documented here.

These skills track the [`@metamask/agentic-cli`](https://github.com/MetaMask/agentic) releases.
Each entry lists the skill `version` (frontmatter) and the CLI `cliVersion` it targets,
along with the user-facing CLI changes that motivated the skill update. Use this log to
catch up if you are on an older skill version — apply the entries above yours in order.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and the skills follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
