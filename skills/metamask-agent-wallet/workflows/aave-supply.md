# Aave V3 supply workflow

Use this workflow to supply (deposit) assets into Aave V3 and earn interest.

## Flow

1. Resolve chain, asset address, and pool address.
2. Check wallet balance.
3. Query the Aave API for the supply transaction.
4. Handle approval if required, then supply.

## Resolve chain and addresses

If the user doesn't specify a chain, ask. Look up the pool address:

| Chain | Chain ID | Pool address |
| --- | --- | --- |
| Ethereum | 1 | `0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2` |
| Polygon | 137 | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` |
| Arbitrum | 42161 | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` |
| Optimism | 10 | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` |
| Avalanche | 43114 | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` |
| Base | 8453 | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` |

Resolve the asset's contract address on the target chain. If the user provides a symbol instead of an address, run `mm token list search --query <SYMBOL> --chain <CHAIN_ID>`.

Aave V3 doesn't accept native ETH on most markets. If the reserve accepts native tokens, use `native` instead of `erc20` in the GraphQL request.

## Check balance

Check that the user has sufficient funds:

```bash
mm wallet balance --chain <CHAIN_ID>
```

If the user doesn't have enough of the supply token or native gas token, check balances on other chains. If the user has assets on the same chain, prompt them to swap. If the user has assets on another chain, prompt them to bridge to the target chain before proceeding.

## Query supply transaction

Get the wallet address and query the Aave V3 GraphQL API for the supply execution plan:

```bash
mm wallet address
```

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "{ supply(request: { market: \"<POOL_ADDRESS>\", amount: { erc20: { currency: \"<ASSET_ADDRESS>\", value: \"<AMOUNT>\" } }, sender: \"<WALLET_ADDRESS>\", chainId: <CHAIN_ID> }) { __typename ... on TransactionRequest { to from data value chainId } ... on ApprovalRequired { reason requiredAmount { value decimals } currentAllowance { value decimals } approval { to from data value chainId } originalTransaction { to from data value chainId } } ... on InsufficientBalanceError { required { value decimals } available { value decimals } } } }"
  }'
```

The `value` in the amount is a human-readable decimal string (e.g., `"42"`, `"0.5"`). The API handles decimal-to-wei conversion.

## Handle response

The API returns one of three response types:

### `TransactionRequest`

The transaction is ready to send. Confirm with the user, then send.

The `value` field in the transaction payload must be `0x`-prefixed hex. For ERC-20 supplies, this is `"0x0"`. For native token supplies, convert the amount to hex using the helper script:

```bash
python3 scripts/amount_to_hex.py <AMOUNT> <DECIMALS>
```

If python3 isn't available, multiply the amount by `10^decimals` manually and convert the result to hex.

```bash
mm wallet send-transaction --chain-id <CHAIN_ID> --payload '{"to":"<TO>","value":"0x0","data":"<DATA>"}' --wait --intent "Supply <AMOUNT> <SYMBOL> to Aave V3 on <CHAIN_NAME>"
```

### `ApprovalRequired`

An ERC-20 approval is needed before supply. Confirm the token being approved, the spender, and the amount with the user. Then send the approval.

```bash
mm wallet send-transaction --chain-id <CHAIN_ID> --payload '{"to":"<APPROVAL_TO>","value":"0x0","data":"<APPROVAL_DATA>"}' --wait --intent "Approve <AMOUNT> <SYMBOL> for Aave V3 Pool <POOL_ADDRESS> on <CHAIN_NAME>"
```

After the approval confirms, send the original supply transaction.

```bash
mm wallet send-transaction --chain-id <CHAIN_ID> --payload '{"to":"<ORIGINAL_TX_TO>","value":"0x0","data":"<ORIGINAL_TX_DATA>"}' --wait --intent "Supply <AMOUNT> <SYMBOL> to Aave V3 on <CHAIN_NAME>"
```

Security note: The Aave API returns `max uint256` (unlimited) as the default approval amount. Tell the user. For better security, construct a limited approval by encoding `approve(address,uint256)` calldata (selector `0x095ea7b3`) with the exact supply amount instead of using the API-provided approval transaction.

### `InsufficientBalanceError`

The user doesn't have enough tokens. Show the required and available amounts, then stop.

## Notes

- After the transaction confirms, the user receives aTokens representing their deposit. Use `aave-positions.md` to verify the updated position.
- To check current supply rates before supplying, see `aave-positions.md`.
