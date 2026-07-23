# Troubleshooting Workflow

Use this workflow when a command fails, hangs, prompts unexpectedly, or behaves differently in a terminal.

## Universal Triage

Run `mm doctor` first to inspect CLI version, skills, environment, and session health in one shot:

```bash
mm doctor
```

If you need more detail, run these in order:

```bash
mm --version
mm auth status
mm <failing-command> --help
```

If `auth status` reports anything other than authenticated, fix authentication before debugging downstream wallet, signing, swap, perps, or predict commands.

## Common Symptoms

| Symptom | Likely cause | Next step |
| --- | --- | --- |
| `mm: command not found` | Binary not installed or not on `PATH` | Check install and PATH |
| Async command returns a polling id and appears stuck | Request was dispatched without `--wait` | Use `mm wallet requests list` or `mm wallet requests watch --polling-id <id>` |
| Auth errors after previously working | Expired token | Check `mm auth status` and session file under `~/.metamask/` |
| `CHAIN_ID_MISMATCH` on typed data | Payload `domain.chainId` differs from `--chain-id` | Align the two chain IDs |
| `MNEMONIC_LOCKED` or `WRONG_PASSWORD` | BYOK mnemonic is encrypted and password was wrong or missing | Set the correct `MM_PASSWORD` environment variable and re-run |
| `ALREADY_ENCRYPTED` on `wallet password set` | Mnemonic already has a password | Use `mm wallet password change` instead |
| `NOT_ENCRYPTED` on `wallet password change/remove` | Mnemonic is not encrypted | Use `mm wallet password set` instead |
| `INSUFFICIENT_FUNDS` | Wallet lacks native gas or token balance | Fund the wallet or use gasless relay (ERC-20 transfers/swaps only on relay-supported chains) |
| `INSUFFICIENT_GAS` | No affordable swap quote; wallet lacks native gas | Fund native gas, or re-quote with `--strategy output` / `--all-quotes` to find a gasless option |
| `GASLESS_UNSUPPORTED` | Gasless relay not available on this chain | Fund native gas or use a different chain |
| `UNSUPPORTED_CHAIN` on swap or predict | Chain not supported for this feature | Run `mm chains list` and use a chain with the required feature |
| `REFUEL_UNSUPPORTED_ROUTE` | `--refuel` used on same-chain swap or native-destination bridge | Drop `--refuel` and re-run |
| `AMOUNT_TOO_LOW` or `AMOUNT_TOO_HIGH` | Amount outside provider's accepted range | Adjust the amount and re-quote |
| `SLIPPAGE_TOO_HIGH` or `SLIPPAGE_TOO_LOW` | Slippage outside accepted range for this route | Adjust `--slippage` and re-quote |
| `UNKNOWN_FLAG` with flag list | Unrecognized CLI flag | Check `mm <command> --help` for valid flags |
| `INVALID_CHAIN` | Unsupported or malformed chain ID | Run `mm chains list`; use chain name, numeric ID, or CAIP-2 (e.g. `eip155:1`) |
| `TRADING_MODE_APPROVAL_REJECTED` or `_EXPIRED` | MFA approval for trading mode change was rejected or timed out | Retry `mm wallet trading-mode set` and approve via MFA |
| `WALLET_POLICY_APPROVAL_REJECTED` or `_EXPIRED` | MFA approval for policy change was rejected or timed out | Retry `mm wallet policy set` and approve via MFA |
| Command hangs on `AWAITING_MFA` | MFA approval needed | Approve via MetaMask Mobile (QR login) or email/dashboard (browser login). For QR login users: the MFA request appears in the notifications menu inside MetaMask Mobile. If push notifications are not showing, check that notifications are enabled in both MetaMask Mobile settings (Settings > Notifications) and at the device level (iOS/Android system settings). The notification permission may have been declined during MetaMask onboarding — re-enable it from the device settings. Regardless of push notification settings, the MFA request is always available in the MetaMask Mobile notifications menu |
| `JOB_TIMEOUT` | Wallet job poll timed out (default 10 minutes) | Approve on your paired device if prompted, or check `mm wallet requests list` before retrying |
| `TX_DENIED` | Transaction was denied via MFA | Retry the command and approve when prompted |
| `TX_EXPIRED` | Transaction MFA approval expired | Retry the command and approve promptly |
| `AUTH_FAILED` after a working session | Session token expired during operation | Run `mm login` to re-authenticate |

## Verbose Logging

Use `--verbose` when a command appears to hang or hides progress:

```bash
mm wallet balance --json --verbose
```

Structured logs and progress lines go to stderr; command results remain on stdout.

## Error Codes

For raw error-code meanings, load `../references/errors.md`. Relay CLI errors verbatim before explaining them.

## Reset Last

Use `mm reset` only after checking version, auth status, and the failing command's help output. Reset clears local session state and should not be the first troubleshooting step. Always ask the user for explicit confirmation before running reset. The command itself also prompts for confirmation; pass `--yes` to skip the prompt in non-interactive sessions.
