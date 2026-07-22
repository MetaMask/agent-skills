# Transfer Commands

Use `transfer` to send native token or ERC-20 tokens from the active wallet.

## `transfer` Command

Transfer native currency or ERC-20 tokens to a recipient address.

### Syntax

```bash
mm transfer --to <address> --amount <value> --chain-id <id> --token <symbol-or-address> [--gas-token <symbol-or-address>] [--wait] [--wallet-timeout <seconds>] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--to` | Yes | Recipient hex address (e.g. 0x742d...f2bD18). ENS is not supported. |
| `--amount` | Yes | Human-readable amount to transfer (e.g. 0.5, 100) |
| `--chain-id` | Yes | EVM chain ID as a positive integer (e.g. 1, 137) |
| `--token` | Yes | Token symbol or ERC-20 contract address (e.g. ETH, USDC, 0xa0b8...). Token symbols are resolved via the token search API |
| `--gas-token` | No | ERC-20 token symbol or contract address to pay gasless relay fees (optional; lowest fee token is chosen when omitted). Only applicable for gasless ERC-20 transfers |
| `--wait` | No | Block until the transfer completes (server-wallet mode only; BYOK returns immediately) |
| `--wallet-timeout` | No | Seconds to wait per wallet job (MFA/signing), max 600; overrides config `walletTimeoutSeconds` |
| `--password` | No | Password to unlock the BYOK mnemonic (BYOK mode only) [env: `MM_PASSWORD`] |

### Example

```bash
mm transfer --to 0x742d...f2bD18 --amount 0.5 --chain-id 1 --token ETH
mm transfer --to 0x742d...f2bD18 --amount 100 --chain-id 137 --token USDC
mm transfer --to 0x742d...f2bD18 --amount 1.0 --chain-id 1 --token ETH --toon
```

## Gasless Transfers

ERC-20 transfers can be routed through a gasless relay when the wallet has insufficient native gas. The CLI automatically detects this and routes through the relay. Use `--gas-token` to specify which ERC-20 token pays the relay fee, or omit it to let the CLI choose the lowest-fee token. Gasless transfers are only available on supported chains. If the chain does not support gasless relay, the CLI returns `GASLESS_UNSUPPORTED`.

Gasless transfers are not supported for native token transfers (e.g. ETH, POL). They only apply to ERC-20 token transfers.

## Notes

- If the chain is not mentioned by the user, ask for the chain.
- Use `mm chains list` to discover supported chain IDs.
- In server-wallet mode, transfer returns a `pollingId` when `--wait` is omitted. See `references/polling.md` to track requests.
- Gasless transfers trigger MFA approval flows. The CLI surfaces MFA instructions when a job enters `AWAITING_MFA` state.
