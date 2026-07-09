# Error codes (master list)

Every error code the CLI emits, with recovery. Per-command tables in the other reference files
are scoped subsets; this file is the single master list. Diagnosis flow: workflows/troubleshooting.md.
Always surface the CLI's own `message` and `hint` verbatim before explaining.

## Auth

| Code | Meaning | Recovery |
| --- | --- | --- |
| `ALREADY_AUTHENTICATED` | Valid session already exists | `mm logout`, then log in again |
| `AUTH_FAILED` | Authentication failed (incl. missing refresh token) | Re-run `mm login browser` or `mm login qr` |
| `AUTH_ERROR` | Generic auth error (incl. missing auth token) | `mm auth status`; if not authenticated, workflows/login.md |
| `TOKEN_INVALID` | Invalid CLI token, token pair, or project ID | Re-run login; paste the full `cliToken:cliRefreshToken` |
| `TOKEN_REFRESH_FAILED` | Failed to refresh token | Re-run login (workflows/login.md) |
| `PAIRING_TIMEOUT` / `PAIRING_EXPIRED` | QR/login pairing timed out or expired | Re-run `mm login qr`; scan promptly |
| `INVALID_OTP` | Invalid one-time password | Re-enter the code; separators `-`/space are tolerated |
| `MWP_TIMEOUT` / `MWP_CANCELLED` | Mobile Wallet Protocol timed out or was cancelled | Re-run `mm login qr`; approve on the phone |
| `LOGOUT_FAILED` | Logout failed (incl. token revoke failure) | Retry `mm logout`; last resort `mm reset` after user approval |

## Validation

| Code | Meaning | Recovery |
| --- | --- | --- |
| `MISSING_FLAG` / `MISSING_INPUT` | Required flag/input absent in headless mode | Re-read the command's Required flags table; add the flag |
| `MISSING_CHAIN` / `MISSING_CHAIN_ID` / `INVALID_CHAIN` | Chain absent or invalid | `mm chains list --toon`; pass a valid `--chain-id` |
| `MISSING_TO` / `INVALID_TO` | Recipient absent or malformed | Ask the user for the full `0x` + 40-hex address |
| `INVALID_DATA` / `INVALID_QUANTITY` / `INVALID_INPUT` | Malformed transaction data / EVM quantity / input | Re-validate against the reference's Value format column |
| `INVALID_LIMIT` | Limit out of range (e.g. `mm tx history --limit`: 1-500) | Follow the CLI hint; pass an in-range integer |
| `INVALID_INTERVAL` / `INVALID_TIMESTAMP` | Bad time interval or timestamp | Use Unix seconds (`date +%s`); see references/price.md |
| `INVALID_ASSET_ID` / `MISSING_ASSET_IDS` / `MISSING_ASSET_TYPE` | CAIP asset ID absent or malformed | Build per references/concepts.md § CAIP identifiers |
| `MISSING_QUERY` | Search query absent | Pass the query (e.g. `--query` for token search) |
| `MISSING_WALLET_REF` | Wallet reference absent | Pass `--id`, `--address`, or `--name` (references/wallet.md) |
| `MISSING_TRANSACTION_PAYLOAD` / `INVALID_TRANSACTION_PAYLOAD` | Tx payload absent or invalid JSON | Single-quote the JSON; see references/transaction.md |
| `MISSING_TYPED_DATA` / `INVALID_TYPED_DATA` | EIP-712 payload absent or invalid | See references/signing.md |
| `CHAIN_ID_MISMATCH` | Typed-data `domain.chainId` ≠ `--chain-id` | Align both to the same chain ID |
| `INVALID_MNEMONIC` | BYOK mnemonic invalid | Re-check `MM_MNEMONIC`; never echo it |

## Wallet

| Code | Meaning | Recovery |
| --- | --- | --- |
| `MISSING_MNEMONIC` / `NO_MNEMONIC` | BYOK mode without a stored mnemonic | Re-run `mm init` with `MM_MNEMONIC` set (references/auth.md) |
| `MNEMONIC_LOCKED` | Unlock failed after max attempts | Set the correct `MM_PASSWORD` env var; retry |
| `WRONG_PASSWORD` | Wrong current password | Set the correct `MM_PASSWORD`; for password commands, re-prompt interactively |
| `ALREADY_ENCRYPTED` | Mnemonic already encrypted | Use `mm wallet password change` |
| `NOT_ENCRYPTED` | Mnemonic not encrypted | Use `mm wallet password set` |
| `PASSWORD_MISMATCH` / `EMPTY_PASSWORD` | Confirmation mismatch or empty password | Re-run the password command in a TTY |
| `WALLET_NOT_FOUND` | Wallet not found | `mm wallet list --toon`; select an existing wallet |
| `WALLET_ERROR` | Wallet/provider error (incl. reverts, insufficient funds, network failures) | `mm wallet balance --toon`; check funds/gas; retry |
| `WALLET_METADATA` | Wallet metadata error | `mm wallet show --toon`; retry |
| `WRONG_NAMESPACE` / `UNSUPPORTED_NAMESPACE` | Bad wallet namespace | Use a supported `--chain-namespace` (references/wallet.md) |
| `NO_AUTH_TOKEN` / `NO_PROJECT_ID` / `MISSING_PROJECT_ID` | Session missing token or project ID | `mm doctor`; re-login (workflows/login.md) |
| `INVALID_TRADING_MODE` | Trading mode not `guard`/`beast` | `mm wallet trading-mode set guard` or `beast` |
| `ALREADY_SET_TRADING_MODE` | Mode already set to that value | Nothing to do; inform the user |

## Command / session

| Code | Meaning | Recovery |
| --- | --- | --- |
| `ABORTED` | User aborted at a prompt | Nothing to do; confirm and retry if intended |
| `NOT_INITIALIZED` | `mm init` not run | workflows/onboarding.md |
| `NO_TTY` | Interactive prompt without a terminal | Pass explicit subcommand/flags; run password prompts in a TTY |
| `MISSING_ID` / `MISSING_QUOTE_ID` / `MISSING_SWAP_PARAMS` | Required ID or swap params absent | Capture the ID from the previous command's output; re-run |
| `COMING_SOON` | Feature not available in this environment | Use an alternative method or environment |
| `INVALID_CONFIG_KEY` / `INVALID_CONFIG_VALUE` | Bad `mm config` key or value | Keys: `env`,`verbose`,`format`,`walletTimeoutSeconds` (references/auth.md) |
| `RESET_FAILED` | Session reset failed | Retry `mm reset`; check `~/.metamask/` permissions |
| `NETWORK_UNREACHABLE` | Network unreachable | Check connectivity; retry |

## Swap & bridge

| Code | Meaning | Recovery |
| --- | --- | --- |
| `NO_QUOTES` | No route for pair/amount | Try another amount/pair; verify the token via `mm token list search` |
| `BRIDGE_API_ERROR` / `SWAP_ERROR` | Backend swap/bridge error | Retry; if persistent, re-quote |
| `TOKEN_NOT_FOUND` | Token unknown on that chain | `mm token list search --query <symbol> --chain <chain-id>` |
| `INVALID_SWAP_PARAMS` | Invalid parameter combination (e.g. `--to-address` on a same-chain swap) | Follow the CLI hint; see references/swap.md |
| `NATIVE_ASSET_UNSUPPORTED` | Native asset unsupported on this route | Use the wrapped token or a different route |
| `QUOTE_PERSIST_FAILED` / `QUOTE_NOT_FOUND` | Quote not saved or expired | Re-run `mm swap quote`; execute promptly by `--quote-id` |
| `EXECUTE_FAILED` / `NO_TRADE_DATA` | Execution failed / no trade data | `mm swap status --quote-id <quote-id>`; re-quote if terminal |
| `STATUS_UNAVAILABLE` | Status not yet available | Wait and re-run `mm swap status` |

## Perps

| Code | Meaning | Recovery |
| --- | --- | --- |
| `UNSUPPORTED_VENUE` / `UNSUPPORTED_NETWORK` / `UNSUPPORTED_ROUTE` / `UNSUPPORTED_ASSET` / `UNSUPPORTED_SOURCE_CHAIN` | Unsupported venue/network/route/asset/chain | `mm perps list-venues --toon`; use supported values (references/perps.md) |
| `INVALID_SYMBOL` | Unknown market symbol | `mm perps markets --toon`; pick a listed symbol |
| `INVALID_AMOUNT` / `INVALID_SIZE` / `INVALID_LEVERAGE` / `INVALID_PRICE` / `INVALID_SLIPPAGE` / `INVALID_ADDRESS` | Malformed numeric/address input | Re-validate against references/perps.md flag tables |
| `INSUFFICIENT_BALANCE` | Not enough margin/balance | `mm perps balance --toon`; offer `mm perps deposit` |
| `POSITION_NOT_FOUND` | No such position | `mm perps positions --toon` |
| `QUOTE_FAILED` / `ORDER_REJECTED` / `CANCEL_FAILED` | Quote/order/cancel rejected | Surface the message; re-quote and retry with user approval |
| `SIGNING_FAILED` | Signing failed | BYOK: set `MM_PASSWORD`; check `mm wallet requests list` |
| `DEPOSIT_FAILED` / `WITHDRAW_FAILED` | Fund move failed | Check balances on both sides; retry |
| `HYPERLIQUID_ERROR` / `PERPS_ERROR` | Venue/generic perps error | Surface verbatim; retry once |

## Predict

| Code | Meaning | Recovery |
| --- | --- | --- |
| `PREDICT_SETUP_REQUIRED` | One-time setup not done | workflows/predict-setup.md |
| `PREDICT_AUTH_REQUIRED` / `PREDICT_AUTH_INVALID` | Predict credentials missing/invalid | `mm predict auth --refresh` (references/predict-account.md) |
| `PREDICT_RELAYER_CONFIG_REQUIRED` | Relayer config required | Re-run `mm predict setup` |
| `PREDICT_INVALID_DEPOSIT_AMOUNT` / `PREDICT_WITHDRAW_ZERO` | Bad deposit/withdraw amount | Ask the user for a positive amount |
| `PREDICT_WITHDRAW_INSUFFICIENT_BALANCE` / `PREDICT_INSUFFICIENT_BALANCE` / `PREDICT_INSUFFICIENT_FUNDING_BALANCE` | Balance too low | `mm predict balance --toon`; offer a deposit (workflows/predict-funding.md) |
| `PREDICT_INSUFFICIENT_ALLOWANCE` | Allowance too low | `mm predict approve` (references/predict-account.md) |
| `PREDICT_FUNDING_CHAIN_UNSUPPORTED` / `UNSUPPORTED_PREDICT_CHAIN` | Chain unsupported for Predict | Use the supported funding chain (references/predict-account.md) |
| `PREDICT_CANCEL_TARGET_REQUIRED` | No cancel target given | Pass `--order-id`, `--market`, `--asset`, or `--all` |
| `PREDICT_WALLET_STATE_REQUIRED` / `PREDICT_METHOD_UNAVAILABLE` | Wallet state missing / method unavailable | `mm predict status --toon`; re-run setup if hinted |
| `PREDICT_DEPOSIT_FAILED` / `PREDICT_ERROR` | Deposit/generic Predict failure | Surface verbatim; check `mm predict status` |
| `PREDICT_GEOBLOCKED` | Region not supported by Polymarket | Confirm with `mm predict geoblock`; Predict is unusable from this location |

## History

| Code | Meaning | Recovery |
| --- | --- | --- |
| `NO_HISTORY_WALLETS` | No EVM wallets in roster | `mm wallet list --toon`; create/select a wallet first |
