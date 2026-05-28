# Transfer Commands

Use `transfer` to send native token or ERC-20 tokens from the active wallet.

## `transfer` Command

Transfer native currency or ERC-20 tokens to a recipient address.

### Syntax

```bash
mm-dev transfer --to <address> --amount <value> --chain-id <id> --token <symbol-or-address> [--wait]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--to` | Yes | Recipient address in Hex. ENS is not supported. |
| `--amount` | Yes | Human readable amount in ETH format. |
| `--chain-id` | Yes | EVM chain ID. |
| `--token` | Yes | Token symbol or ERC-20 contract address |
| `--wait` | No | Wait for the transfer request to finish |

### Example

```bash
mm-dev transfer --to 0x742d...f2bD18 --amount 0.5 --chain-id 1 --token ETH
mm-dev transfer --to 0x742d...f2bD18 --amount 100 --chain-id 137 --token USDC
mm-dev transfer --to 0x742d...f2bD18 --amount 1.0 --chain-id 1 --token ETH --toon
```

## Notes

- If the Chain is not mentioned by the user, ask for the chain for transfer.
- In server-wallet mode, transfer returns a `pollingId` when `--wait` is omitted. See `references/polling.md` to track requests.
