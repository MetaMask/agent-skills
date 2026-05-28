# Transaction Commands

Use `wallet send-transaction` to send raw EVM transactions with the active wallet.

## `wallet send-transaction` Command

Send a raw EVM transaction using the active wallet.

### Syntax

```bash
mm-dev wallet send-transaction --chain-id <id> --payload '<JSON>' [--wait]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--chain-id` | Yes | EVM chain ID (e.g. `1` for Ethereum, `137` for Polygon) |
| `--payload` | Yes | Transaction JSON (to, value, data, gas params) |
| `--wait` | No | Wait for the transaction request to finish |

### Example

```bash
mm-dev wallet send-transaction --chain-id 1 --payload '{"to":"0x742d...","value":"1000000000000000000","data":"0x"}'
mm-dev wallet send-transaction --chain-id 1 --payload '{"to":"0x...","value":"0","data":"0xabcdef"}' --wait
mm-dev wallet send-transaction --chain-id 1 --payload '...' --toon
```

## Transaction Payload

The `--payload` flag takes a JSON string with transaction fields:

```json
{
  "to": "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18",
  "value": "1000000000000000000",
  "data": "0x"
}
```

Optional fields: `gasLimit`, `gasPrice`, `maxFeePerGas`, `maxPriorityFeePerGas`.

## Notes

- In server-wallet mode, send-transaction returns a `pollingId` when `--wait` is omitted. See `references/polling.md` to track requests.
