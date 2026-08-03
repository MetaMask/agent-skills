# Error Codes

This reference lists error codes the CLI actually emits. SDK-only or remapped codes are noted where relevant. Workflows for diagnosing failures live in `../workflows/troubleshooting.md`.

## Auth Errors

| Code | Meaning |
| --- | --- |
| `ALREADY_AUTHENTICATED` | Valid session already exists; run `mm logout` before logging in again |
| `AUTH_FAILED` | Authentication failed (includes missing refresh token cases) |
| `AUTH_ERROR` | Generic authentication error (includes missing auth token cases) |
| `TOKEN_INVALID` | Invalid CLI token, token pair, or project ID |
| `TOKEN_REFRESH_FAILED` | Failed to refresh token |
| `PAIRING_TIMEOUT` | Login pairing timed out |
| `PAIRING_EXPIRED` | Pairing session expired |
| `INVALID_OTP` | Invalid one-time password |
| `MWP_TIMEOUT` | Mobile Wallet Protocol timeout |
| `MWP_CANCELLED` | Mobile Wallet Protocol cancelled (pairing aborted) |
| `LOGOUT_FAILED` | Logout operation failed (includes token revoke failures) |
| `ALREADY_LOGGED_OUT` | No active session to sign out of. Run `mm login` to authenticate |

## Validation Errors

| Code | Meaning |
| --- | --- |
| `MISSING_FLAG` | Required flag is missing in headless mode |
| `MISSING_INPUT` | Required input is missing |
| `MISSING_CHAIN` | Chain value is missing |
| `MISSING_CHAIN_ID` | Chain ID is missing |
| `INVALID_CHAIN` | Chain value is invalid |
| `MISSING_TO` | Recipient address is missing |
| `INVALID_TO` | Recipient address is invalid |
| `INVALID_DATA` | Transaction data is invalid |
| `INVALID_INPUT` | Invalid user input |
| `UNKNOWN_FLAG` | Unrecognized CLI flag; the error lists valid flags for the command |
| `MISSING_ARG` | Required positional argument is missing |
| `UNEXPECTED_ARG` | Unexpected positional argument provided |
| `INVALID_QUANTITY` | EVM quantity is invalid |
| `INVALID_LIMIT` | Invalid limit value |
| `INVALID_INTERVAL` | Invalid time interval |
| `INVALID_TIMESTAMP` | Invalid timestamp |
| `INVALID_ASSET_ID` | Invalid asset identifier |
| `MISSING_ASSET_IDS` | Missing asset IDs |
| `MISSING_ASSET_TYPE` | Missing asset type |
| `MISSING_QUERY` | Missing search query |
| `MISSING_WALLET_REF` | Missing wallet reference |
| `MISSING_TRANSACTION_PAYLOAD` | Transaction payload is missing |
| `INVALID_TRANSACTION_PAYLOAD` | Transaction payload is invalid |
| `MISSING_TYPED_DATA` | EIP-712 typed data payload is missing |
| `INVALID_TYPED_DATA` | EIP-712 typed data payload is invalid |
| `CHAIN_ID_MISMATCH` | Typed-data domain chain ID differs from `--chain-id` |
| `UNKNOWN_CHAIN` | Unrecognized chain ID |
| `UNSUPPORTED_CHAIN` | The command is not supported on this chain. Run `mm chains list` to see supported chains and their features |
| `INVALID_GAS_TOKEN` | Invalid gas token symbol or address |
| `TOKEN_NO_ADDRESS` | Token symbol could not be resolved to a contract address |
| `INVALID_EVM_ADDRESS` | Invalid EVM address (e.g. malformed transfer recipient) |
| `INVALID_AMOUNT` | Non-positive or malformed amount value |
| `INVALID_MNEMONIC` | BYOK mnemonic is invalid |

## Wallet Errors

| Code | Meaning |
| --- | --- |
| `MISSING_MNEMONIC` | BYOK wallet mode is missing a mnemonic |
| `MNEMONIC_LOCKED` | Mnemonic unlock failed after maximum attempts |
| `WRONG_PASSWORD` | Current password is incorrect |
| `ALREADY_ENCRYPTED` | Mnemonic is already password-encrypted (use `wallet password change` instead) |
| `NOT_ENCRYPTED` | Mnemonic is not encrypted (use `wallet password set` instead) |
| `PASSWORD_MISMATCH` | Password confirmation does not match |
| `EMPTY_PASSWORD` | Empty password provided |
| `WALLET_NOT_FOUND` | Wallet not found |
| `WALLET_ERROR` | Wallet provider or wallet operation error (includes on-chain reverts and network failures from wallet paths) |
| `WALLET_METADATA` | Wallet metadata error |
| `WALLET_NOT_REGISTERED` | Server-side BYOK wallet registration failed. Re-run `mm init --wallet byok` |
| `WRONG_NAMESPACE` | Wrong namespace for wallet |
| `UNSUPPORTED_NAMESPACE` | Unsupported wallet namespace |
| `NO_AUTH_TOKEN` | Missing authentication token for wallet operations |
| `NO_PROJECT_ID` | Project ID not configured for wallet |
| `MISSING_PROJECT_ID` | Project ID is not configured |
| `INVALID_TRADING_MODE` | Invalid trading mode; use `guard` or `beast` |
| `ALREADY_SET_TRADING_MODE` | Trading mode is already set to the requested value |
| `WRONG_WALLET_MODE` | Operation not supported in the current wallet mode |
| `WALLET_MODE_APPROVAL_IN_PROGRESS` | A wallet mode change approval is already in progress |
| `TRADING_MODE_APPROVAL_REJECTED` | Trading mode change was rejected via MFA |
| `TRADING_MODE_APPROVAL_EXPIRED` | Trading mode change MFA approval expired |
| `WALLET_POLICY_APPROVAL_IN_PROGRESS` | A wallet policy change approval is already in progress |
| `WALLET_POLICY_APPROVAL_REJECTED` | Wallet policy change was rejected via MFA |
| `WALLET_POLICY_APPROVAL_EXPIRED` | Wallet policy change MFA approval expired |
| `INSUFFICIENT_FUNDS` | Insufficient native balance or token balance for the operation |

## Command Errors

| Code | Meaning |
| --- | --- |
| `ABORTED` | Operation aborted by user |
| `JOB_TIMEOUT` | Wallet job poll timed out. Approve on your paired device if prompted, or check `mm wallet requests list` before retrying |
| `REQUEST_NOT_FOUND` | Wallet job/request not found on remote |
| `TX_DENIED` | Transaction was denied via MFA |
| `TX_EXPIRED` | Transaction MFA approval expired |
| `TX_FAILED` | Transaction failed after submission |
| `TX_REVERTED` | Transaction reverted on-chain (RPC revert); check the `failure_reason` field for details |
| `RELAY_TIMEOUT` | Gasless relay poll timed out. Check `mm wallet requests watch --polling-id <id>` before retrying; the job may still complete |
| `NOT_INITIALIZED` | Project not initialized. Run `mm init` |
| `NO_MNEMONIC` | Mnemonic not stored |
| `NO_TTY` | No TTY available for interactive prompts |
| `MISSING_ID` | Missing ID parameter |
| `MISSING_QUOTE_ID` | Missing quote ID |
| `MISSING_SWAP_PARAMS` | Missing swap parameters |
| `TX_NOT_FOUND` | Transaction not found for the given hash |
| `INVALID_TX_HASH` | Invalid transaction hash format |
| `COMING_SOON` | Feature not yet available (e.g. `mm login qr` on production) |
| `INVALID_CONFIG_KEY` | Unknown config key passed to `mm config get` or `mm config set` |
| `INVALID_CONFIG_VALUE` | Invalid value for a config key (e.g. env not in `prod|dev|uat`) |

## Swap & Bridge Errors

| Code | Meaning |
| --- | --- |
| `NO_QUOTES` | No swap or bridge quotes available. When returned as a soft unavailable outcome (exit 0), adjust amount, slippage, or token and retry |
| `QUOTE_RETRY` | Transient bridge hiccup — re-run the exact same quote to get routes |
| `BRIDGE_API_ERROR` | Bridge API error |
| `TOKEN_NOT_FOUND` | Token not found |
| `TOKEN_NOT_SUPPORTED` | Token not supported for this swap route |
| `INVALID_SWAP_PARAMS` | Invalid swap parameters (includes `--all-quotes` and `--yes` used together) |
| `NATIVE_ASSET_UNSUPPORTED` | Native asset not supported for this swap route |
| `INSUFFICIENT_GAS` | Insufficient native gas to cover the swap; add native gas or use `--strategy output` / `--all-quotes` to pick a gasless quote |
| `REFUEL_UNSUPPORTED_ROUTE` | Refuel is not supported on this route (same-chain or native destination token). Drop `--refuel` and re-run |
| `AMOUNT_TOO_HIGH` | Amount too high for available liquidity |
| `AMOUNT_TOO_LOW` | Amount below provider minimum |
| `SLIPPAGE_TOO_HIGH` | Slippage too high for this route |
| `SLIPPAGE_TOO_LOW` | Slippage too low for this route |
| `RWA_GEO_RESTRICTED` | RWA asset not available in your region |
| `RWA_NATIVE_TOKEN_UNSUPPORTED` | RWA cannot be swapped against native asset |
| `RWA_MARKET_UNAVAILABLE` | RWA market temporarily unavailable |
| `QUOTE_PERSIST_FAILED` | Failed to persist quote |
| `QUOTE_NOT_FOUND` | Quote not found |
| `EXECUTE_FAILED` | Swap execution failed |
| `NO_TRADE_DATA` | No trade data available |
| `STATUS_UNAVAILABLE` | Swap status unavailable |
| `GASLESS_UNSUPPORTED` | Gasless relay is not supported on this chain |
| `GASLESS_NOT_CONFIGURED` | Gasless relay is not configured for this operation |
| `INSUFFICIENT_FUNDS` | Insufficient source token balance to execute swap. Check `mm wallet balance`, fund the wallet, or lower `--amount` and re-quote |
| `SWAP_ERROR` | Generic swap error |

## Perps Errors

| Code | Meaning |
| --- | --- |
| `UNSUPPORTED_VENUE` | Unsupported perpetual venue |
| `UNSUPPORTED_NETWORK` | Unsupported network for perps |
| `UNSUPPORTED_ROUTE` | Unsupported deposit or withdraw route |
| `UNSUPPORTED_ASSET` | Unsupported asset |
| `UNSUPPORTED_SOURCE_CHAIN` | Unsupported source chain for perps deposit |
| `INVALID_SYMBOL` | Unknown perpetual market symbol |
| `INVALID_AMOUNT` | Invalid amount |
| `INVALID_SIZE` | Invalid position size |
| `INVALID_LEVERAGE` | Invalid leverage value |
| `INVALID_PRICE` | Invalid price |
| `INVALID_SLIPPAGE` | Invalid slippage value |
| `INVALID_ADDRESS` | Invalid address |
| `INSUFFICIENT_BALANCE` | Insufficient balance |
| `POSITION_NOT_FOUND` | Position not found |
| `QUOTE_FAILED` | Quote generation failed |
| `ORDER_REJECTED` | Order rejected |
| `CANCEL_FAILED` | Order cancellation failed |
| `SIGNING_FAILED` | Signing operation failed |
| `WITHDRAW_FAILED` | Withdrawal failed |
| `DEPOSIT_FAILED` | Deposit failed |
| `RATE_LIMITED` | Rate-limited by the venue (e.g. Hyperliquid HTTP 429). Wait and retry |
| `HYPERLIQUID_ERROR` | Hyperliquid protocol error |
| `PERPS_ERROR` | Generic perpetuals error |

## Predict Errors

| Code | Meaning |
| --- | --- |
| `PREDICT_SETUP_REQUIRED` | Predict setup required before operation. Run `mm predict setup` for this owner, then retry |
| `PREDICT_AUTH_REQUIRED` | Predict authentication required. Run `mm predict auth`, then retry |
| `PREDICT_AUTH_INVALID` | Predict credentials invalid or incomplete. Run `mm predict auth --refresh`, then retry |
| `PREDICT_RELAYER_CONFIG_REQUIRED` | Relayer configuration required. Configure the Predict relayer URL and retry |
| `PREDICT_INVALID_DEPOSIT_AMOUNT` | Invalid deposit amount. Pass a positive pUSD amount with up to 6 decimal places |
| `PREDICT_WITHDRAW_ZERO` | Withdraw amount must be greater than zero. Pass a `--amount` greater than zero |
| `PREDICT_WITHDRAW_INSUFFICIENT_BALANCE` | Withdraw amount exceeds deposit wallet pUSD balance. Lower `--amount` or check `mm predict balance` |
| `PREDICT_FUNDING_CHAIN_UNSUPPORTED` | Funding chain not supported. Deposit funding is only configured for Polygon (137) |
| `PREDICT_INSUFFICIENT_BALANCE` | Insufficient Predict balance. Lower `--size`, or deposit more collateral with `mm predict deposit`; check `mm predict balance` |
| `PREDICT_INSUFFICIENT_ALLOWANCE` | Insufficient Predict allowance. Run `mm predict approve`, then retry the order |
| `PREDICT_INSUFFICIENT_FUNDING_BALANCE` | Insufficient funding balance for Predict deposit. Fund the deposit wallet with USDC.e, or lower the deposit amount |
| `PREDICT_CANCEL_TARGET_REQUIRED` | Cancel target not specified. Pass `orderId`, `orderIds`, market/assetId, or `--all` |
| `PREDICT_ORDER_SIZE_TOO_SMALL` | Order size is below the exchange minimum. Raise `--size` to at least the minimum stated in the error; inspect liquidity with `mm predict book` |
| `PREDICT_ORDER_NOT_FILLED` | Order could not be fully filled. Adjust `--size`/`--price`, check liquidity with `mm predict book`, or use GTC instead of FOK |
| `PREDICT_REDEEM_NONE` | No redeemable positions. Check `mm predict redeem list` |
| `PREDICT_REDEEM_NOT_FOUND` | Redeem target not found. Check the condition/token ID against `mm predict redeem list` |
| `PREDICT_REDEEM_MISSING_TARGET` | Missing redeem target. Pass a condition or token ID |
| `PREDICT_WALLET_STATE_REQUIRED` | Wallet state required for Predict |
| `PREDICT_METHOD_UNAVAILABLE` | Predict method not available |
| `PREDICT_DEPOSIT_FAILED` | Predict deposit failed |
| `PREDICT_ERROR` | Generic Predict error. Re-check inputs and mode (`mm predict mode`); run `mm predict status` to verify back-end reachability |
| `PREDICT_INSUFFICIENT_GAS` | Insufficient native POL for gas on Polygon. Top up wallet with POL, check balances with `mm wallet balance`, then retry |
| `PREDICT_GEOBLOCKED` | Polymarket is not available in your region; Predict features cannot be used from this location. Emitted by `mm predict setup` (region guard) and surfaced by `mm predict geoblock` |
| `UNSUPPORTED_PREDICT_CHAIN` | Predict chain not supported |

## Earn Errors

| Code | Meaning |
| --- | --- |
| `VAULT_NOT_FOUND` | No matching vault found for the token/chain/protocol |
| `NOT_REDEEMABLE` | Vault does not support withdrawals |
| `EARN_API_ERROR` | LiFi API error or rate limit |
| `QUOTE_FAILED` | LiFi returned no executable transaction |
| `EXECUTE_FAILED` | Transaction reverted, no hash returned, or cross-chain timeout |
| `EARN_ERROR` | Generic earn error |

## Transaction History Errors

| Code | Meaning |
| --- | --- |
| `NO_HISTORY_WALLETS` | No EVM wallets found in roster for transaction history |

## Network & Filesystem Errors

| Code | Meaning |
| --- | --- |
| `NETWORK_UNREACHABLE` | Network unreachable |
| `NETWORK_TIMEOUT` | Network request timed out |
| `RESET_FAILED` | Failed to reset CLI session |
| `MNEMONIC_STORE_FAILED` | Failed to store mnemonic to disk |
| `FILESYSTEM_ERROR` | Generic filesystem error |
