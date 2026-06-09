# Aave V3 repay workflow

Use this workflow to repay borrowed assets on Aave V3.

## Flow

1. Resolve chain, asset address, and pool address.
2. Check outstanding debt.
3. Query the Aave API for the repay transaction.
4. Handle approval if required, then repay.

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

## Check debt

Query the user's outstanding debt using `userBorrows` from `aave-positions.md`. Identify the following.

- The asset being repaid and its contract address
- Current debt amount (`debt.amount.value`)
- Current borrow APY (`apy.formatted`)

Show the debt amount and current rate.

## Query repay transaction

Get the wallet address and query the Aave V3 GraphQL API:

```bash
mm wallet address
```

For a specific repayment amount:

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "{ repay(request: { market: \"<POOL_ADDRESS>\", amount: { erc20: { currency: \"<ASSET_ADDRESS>\", value: { exact: \"<AMOUNT>\" } } }, sender: \"<WALLET_ADDRESS>\", chainId: <CHAIN_ID> }) { __typename ... on TransactionRequest { to from data value chainId } ... on ApprovalRequired { reason requiredAmount { value decimals } currentAllowance { value decimals } approval { to from data value chainId } originalTransaction { to from data value chainId } } ... on InsufficientBalanceError { required { value decimals } available { value decimals } } } }"
  }'
```

To repay the full debt, use `{ max: true }` instead of `{ exact: \"<AMOUNT>\" }` in the value field. This lets the contract calculate the exact outstanding debt at execution time, including accrued interest.

You can't use `{ max: true }` when `onBehalfOf` is set in the request. If repaying on behalf of another address, specify the exact repayment amount. Query the current debt via `userBorrows` and add a small buffer (e.g., 0.5%) to account for interest accrued between query and execution.

## Handle response

The API returns one of three response types:

### `TransactionRequest`

The transaction is ready to send. Confirm with the user, then send. The `value` field must be `0x`-prefixed hex (typically `"0x0"` for ERC-20 repayments).

```bash
mm wallet send-transaction --chain-id <CHAIN_ID> --payload '{"to":"<TO>","value":"0x0","data":"<DATA>"}' --wait --intent "Repay <AMOUNT> <SYMBOL> on Aave V3 on <CHAIN_NAME>"
```

### `ApprovalRequired`

An ERC-20 approval is needed before repayment. Confirm the token being approved, the spender, and the amount with the user. Then send the approval.

```bash
mm wallet send-transaction --chain-id <CHAIN_ID> --payload '{"to":"<APPROVAL_TO>","value":"0x0","data":"<APPROVAL_DATA>"}' --wait --intent "Approve <AMOUNT> <SYMBOL> for Aave V3 Pool <POOL_ADDRESS> on <CHAIN_NAME>"
```

After the approval confirms, send the original repay transaction.

```bash
mm wallet send-transaction --chain-id <CHAIN_ID> --payload '{"to":"<ORIGINAL_TX_TO>","value":"0x0","data":"<ORIGINAL_TX_DATA>"}' --wait --intent "Repay <AMOUNT> <SYMBOL> on Aave V3 on <CHAIN_NAME>"
```

ERC-20 approvals are consumed by the repay transaction. If the user approved an exact amount and needs to repay again (e.g., for remaining dust debt), a new approval is required. Consider approving slightly more than the debt amount to avoid this.

### `InsufficientBalanceError`

The user doesn't have enough tokens to repay. Show the required and available amounts, then stop.

## Handling dust debt

Interest accrues continuously between borrow and repay transactions. When repaying an exact amount equal to the original borrow, a small "dust" debt remains.

To handle this:
1. Use `{ max: true }` (only works without `onBehalfOf`) to let the contract calculate the exact outstanding debt at execution time.
2. Over-repay slightly: query the current debt via `userBorrows`, then repay with the debt amount plus a small buffer (e.g., 0.5%). The contract only deducts the actual debt and refunds the excess.
3. Acquire more tokens: if the wallet balance equals the exact original borrow amount, acquire slightly more of the token to cover interest.

## Notes

- After the transaction confirms, use `aave-positions.md` to verify the debt is cleared or reduced.
- All debt (including dust amounts) must be cleared before a full collateral withdrawal. See `aave-withdraw.md`.
