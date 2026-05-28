# Error Codes

This reference lists raw CLI and SDK error codes. Workflows for diagnosing failures live in `../workflows/troubleshooting.md`.

## Auth Errors

| Code | Meaning |
| --- | --- |
| `PAIRING_ABORTED` | Login pairing was aborted |
| `PAIRING_TIMEOUT` | Login pairing timed out |
| `INVALID_CLI_TOKENS` | CLI token pair is invalid |
| `INVALID_CLI_TOKEN` | CLI token is invalid |
| `MISSING_REFRESH_TOKEN` | Refresh token is missing |
| `REFRESH_CLI_TOKEN_FAILED` | CLI token refresh failed |
| `MISSING_TOKEN` | Required auth token is missing |
| `REVOKE_CLI_TOKEN_FAILED` | CLI token revoke failed |
| `INVALID_PROJECT_ID` | Project ID is invalid for the selected environment |

## Validation Errors

| Code | Meaning |
| --- | --- |
| `MISSING_FLAG` | Required flag is missing in headless mode |
| `MISSING_INPUT` | Required input is missing |
| `MISSING_CHAIN` | Chain value is missing |
| `INVALID_CHAIN` | Chain value is invalid |
| `MISSING_TO` | Recipient address is missing |
| `INVALID_TO` | Recipient address is invalid |
| `INVALID_DATA` | Transaction data is invalid |
| `INVALID_QUANTITY` | EVM quantity is invalid |
| `MISSING_TRANSACTION_PAYLOAD` | Transaction payload is missing |
| `INVALID_TRANSACTION_PAYLOAD` | Transaction payload is invalid |
| `MISSING_TYPED_DATA` | EIP-712 typed data payload is missing |
| `INVALID_TYPED_DATA` | EIP-712 typed data payload is invalid |
| `CHAIN_ID_MISMATCH` | Typed-data domain chain ID differs from `--chain-id` |
| `INVALID_MNEMONIC` | BYOK mnemonic is invalid |

## Wallet Errors

| Code | Meaning |
| --- | --- |
| `MISSING_MNEMONIC` | BYOK wallet mode is missing a mnemonic |
| `WALLET_ERROR` | Wallet provider or wallet operation error |

## Examples

```bash
mm-dev auth status --json
mm-dev wallet sign-typed-data --chain-id 1 --payload '{"types":{},"primaryType":"Permit","domain":{"chainId":137},"message":{}}'
```
