# Changelog

All notable changes to the MetaMask Agent CLI Skills are documented here.

These skills track the [`@metamask/agentic-cli`](https://github.com/MetaMask/agentic) releases.
Each entry lists the skill `version` (frontmatter) and the CLI `cliVersion` it targets,
along with the user-facing CLI changes that motivated the skill update. Use this log to
catch up if you are on an older skill version — apply the entries above yours in order.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and the skills follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [6.0.0] — targets CLI v4.0.1

### Changed (breaking)

- **Full rewrite of `SKILL.md` and every file in `references/` and `workflows/`** to fixed,
  weak-LLM-friendly templates: one canonical syntax per command (flag form wherever both
  positional and flag forms exist), required/optional flag tables with value-format columns,
  captured real output blocks with `Capture: field → <placeholder>` lines, explicit
  "Confirm before executing" field checklists, per-file error/recovery tables, and a
  placeholder legend + global-flags table centralized in `SKILL.md`. Every documented flag was
  verified against `mm <command> --help` JSON on CLI v4.0.1. Incremental catch-up from ≤5.x
  does not apply to this entry — re-read the whole skill.
- Split `references/predict.md` → `predict-account.md`, `predict-data.md`, `predict-trade.md`;
  split `references/market-data.md` → `price.md`, `token.md`; renamed `references/chain.md` →
  `chains.md` and `references/polling.md` → `wallet-requests.md`.

### Added

- `references/concepts.md` — shared concepts: wallet/trading modes, async job model
  (`pollingId`, `--wait`, `intent`), secrets via `MM_PASSWORD`/`MM_MNEMONIC`, `$SKILL_DIR`,
  CAIP-2/CAIP-19 construction, amount/decimals conversion, suspicious-payload checklist.
- `references/aave.md` — canonical home for the Aave V3 GraphQL machinery (endpoint, market
  discovery, amount formats per operation, the three response types, approval security rule).
- `scripts/encode_approve.py` — deterministic ERC-20 `approve(address,uint256)` calldata for
  exact-amount allowances (replaces the old hand-encoding instruction in the supply workflow).

### Fixed

- Removed phantom positional syntax: `predict quote`/`place`/`markets get` and
  `wallet requests watch` are flag-only (`--token-id`, `--market`, `--polling-id`).
- `predict redeem`: exactly one of `<condition-id>` | `--all` (previously shown as both optional).
- `predict markets search` takes a positional query (`mm predict markets search <query>`).
- Documented `--wallet-timeout` on all wallet-job commands and the `walletTimeoutSeconds`
  config key; `MM_PASSWORD` env applies to every command that accepts `--password`.
- perps: `--venue` is optional (defaults to `hyperliquid`); `--dry-run`/`--yes` documented on
  cancel/transfer/deposit/withdraw (the old "`--yes` has no effect" claim was false).
- `transfer --token`: ERC-20 transfers use the contract address; symbols only for native.
- QR login (`mm login qr`) works on all environments including production — the
  `COMING_SOON`-on-prod claim in the onboarding workflow was stale (verified against CLI source).
- `--to-address` is rejected for same-chain swaps (`INVALID_SWAP_PARAMS`) — documented with the
  verbatim error; `--to-address`/`--refuel` are cross-chain only.
- Aave supply: explicit ERC-20 (`"value":"0x0"`) vs native (hex from `amount_to_hex.py`)
  branch; per-operation amount formats consolidated in `references/aave.md`.
- SKILL.md routing: added `mm tx` (lookup by hash); replaced the vague `mm price ...` /
  `mm token ...` rows with one row per subcommand.

### Notes

- The CLI's own `--help` *usage strings* are unreliable in places (e.g.
  `mm wallet trading-mode get --help` prints `mm mode get`, which does not exist, and
  advertises `--chain-namespace`/`--address` flags that are rejected). The docs trust the
  `flags` arrays and empirical runs instead; upstream bug to file against MetaMask/agentic.

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
