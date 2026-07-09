# Aave V3 (GraphQL API + mm wallet send-transaction)

The `mm` CLI has no Aave commands. Aave flows query the Aave V3 GraphQL API for a ready-made
transaction, then execute it with `mm wallet send-transaction`. This file is the shared
machinery; per-operation steps live in workflows/aave-supply.md, aave-withdraw.md,
aave-borrow.md, aave-repay.md, aave-collateral.md, aave-positions.md, aave-markets.md.

## Prerequisites

- `mm doctor` reports `authenticated: true` and `initialized: true` (SKILL.md § Preflight).
- If the user did not name a chain, ask — do not guess. Chain IDs: `mm chains list`.
- Sender address comes from `mm wallet address --toon` (capture `address` → `<address>`).
- Asset symbols resolve to contract addresses with `mm token list search --query <symbol> --chain <chain-id>` (references/token.md).

## Endpoint

All queries are POSTs to `https://api.v3.aave.com/graphql`:

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"<graphql-query>"}'
```

## Market discovery (run first in every flow)

```bash
curl -s -X POST https://api.v3.aave.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ markets(request: { chainIds: [8453] }) { address reserves { underlyingToken { symbol } } } }"}'
```

### Output

```json
{"data":{"markets":[{"address":"0xA238Dd80C259a72e81d7e4664a9801593F98d1c5",
"reserves":[{"underlyingToken":{"symbol":"USDC"}},{"underlyingToken":{"symbol":"WETH"}},
{"underlyingToken":{"symbol":"cbBTC"}}]}]}}
```

Capture: `markets[].address` → `<pool-address>`.

1. One market returned → use its `address` as `<pool-address>`.
2. Multiple markets returned → show the user each `address` with up to 5 of its reserve
   symbols and ask which market to use.

## Amount format per operation

The GraphQL `amount` field format differs by operation. Use exactly:

| Operation | `amount` value format |
| --- | --- |
| `supply` | `value: "<amount>"` (plain decimal string, e.g. `"0.5"`) |
| `borrow` | `value: "<amount>"` (plain decimal string) |
| `withdraw` | `value: { exact: "<amount>" }`, or `value: { max: true }` for the full balance |
| `repay` | `value: { exact: "<amount>" }`, or `value: { max: true }` for the full debt (not allowed with `onBehalfOf`) |
| `healthFactorPreview` | same format as the wrapped operation |

Amounts are human-readable decimals; the API converts to atomic units. ERC-20 asset:
`amount: { erc20: { currency: "<address>", value: ... } }`. Native token (only where the
reserve accepts it): use `native` in place of `erc20` (no `currency` field).

## Response types (supply / withdraw / borrow / repay)

Every operation query returns one of three `__typename`s. Handle in order:

1. `TransactionRequest` (`{to, from, data, value, chainId}`) → confirm with the user, then
   execute it (see "Executing" below).
2. `ApprovalRequired` → an ERC-20 allowance is needed first. It contains `approval`
   (a TransactionRequest) and `originalTransaction` (the operation itself). Apply the
   approval security rule below, confirm with the user, send the approval, wait for it to
   complete, then send `originalTransaction`.
3. `InsufficientBalanceError` (`{required, available}`) → show both amounts to the user and
   stop.

## Executing a returned transaction

```bash
mm wallet send-transaction --chain-id <chain-id> --payload '{"to":"<address>","value":"<hex>","data":"<calldata>"}' --wait --intent "<human-readable summary>" --toon
```

`--payload` fields come from the API response, except `value`, which must be `0x`-prefixed hex:

- ERC-20 operation (supply/withdraw/borrow/repay/approval of a token) → `"value":"0x0"`.
- Native-token supply → `"value":"<hex>"` from:

```bash
python3 "$SKILL_DIR/scripts/amount_to_hex.py" 0.5 18
# -> 0x6f05b59d3b20000
```

Always pass `--wait` and a human-readable `--intent`. Global flags and `--wallet-timeout`
apply — see SKILL.md § Global flags. BYOK with an encrypted mnemonic: set `MM_PASSWORD`
first (references/concepts.md). Async model and pollingId tracking: references/concepts.md.

## Approval security rule

The API's default `approval` transaction grants an UNLIMITED allowance (max uint256).

1. Tell the user the API default is an unlimited approval.
2. Offer the exact-amount alternative — encode the calldata yourself:

```bash
python3 "$SKILL_DIR/scripts/encode_approve.py" 0xA238Dd80C259a72e81d7e4664a9801593F98d1c5 100 6
# -> 0x095ea7b3000000000000000000000000a238dd80c259a72e81d7e4664a9801593f98d1c50000000000000000000000000000000000000000000000000000000005f5e100
```

Arguments: spender (`<pool-address>`), amount, token decimals. Use the printed calldata as
`"data"` and the TOKEN CONTRACT address as `"to"` (`"value":"0x0"`). Exact-amount approvals
are consumed by the operation; a repeat operation needs a fresh approval.

## Confirm before executing

Show the user ALL of: operation, asset symbol + contract address, amount (or "full
balance"/"full debt"), chain, pool address, and — for approvals — the spender and whether
the allowance is unlimited or exact. Do not run until the user approves.

## Errors

| Code | Cause | Recovery |
| --- | --- | --- |
| `InsufficientBalanceError` (API) | Not enough tokens for the operation | Show `required` vs `available`; offer a swap (workflows/swap.md) or bridge (workflows/bridge.md) |
| GraphQL `errors[]` in response | Malformed query or unsupported market/asset | Re-check pool address, asset address, chain ID, and the amount format table above |
| Revert `0x6679996d` | Full withdrawal attempted with outstanding debt | Repay all debt first (workflows/aave-repay.md) |
| `WALLET_ERROR` | Insufficient gas at execution | `mm wallet balance --chain <chain-id>`; top up the native token |
| `NOT_INITIALIZED` | Project has no wallet mode | Follow workflows/onboarding.md, then retry |

Full code list: references/errors.md.
