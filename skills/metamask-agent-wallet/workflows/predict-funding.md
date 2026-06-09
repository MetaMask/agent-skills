# Predict funding workflow

Use this workflow to deposit or withdraw pUSD from the Predict deposit wallet.

Reference command syntax in `references/predict.md`.

## Flow

1. Check deposit wallet balance.
2. Deposit or withdraw.

## Check deposit wallet balance

```bash
mm predict balance --sync
```

## Deposit

If the user doesn't specify an amount, ask how much they want to deposit. Then check the user's Polygon balance for USDC.e and POL.

```bash
mm wallet balance --chain 137
```

### No POL and no USDC.e

Tell the user to acquire POL on Polygon first. Without POL, no on-chain transaction is possible. Check if the user has tokens on another chain to bridge POL from.

```bash
mm swap quote --from <TOKEN> --to POL --amount 1 --from-chain <SOURCE_CHAIN_ID> --to-chain 137
```

Once the user has POL, swap to USDC.e.

```bash
mm swap quote --from POL --to USDC.e --amount <AMOUNT> --from-chain 137
```

### Has POL but not enough to swap for USDC.e

If the user's POL balance is too low for a swap, bridge USDC.e from another chain.

```bash
mm swap quote --from <TOKEN> --to USDC.e --amount <AMOUNT> --from-chain <SOURCE_CHAIN_ID> --to-chain 137
```

### Has enough POL or other tokens on Polygon

Swap directly into USDC.e.

```bash
mm swap quote --from <TOKEN> --to USDC.e --amount <AMOUNT> --from-chain 137
```

After the bridge or swap completes, re-check the balance before proceeding.

### Execute deposit

```bash
mm predict deposit --amount <AMOUNT> --wait
```

`--amount` is in USDC.e. The CLI converts USDC.e to pUSD in the deposit wallet upon deposit. The owner EOA needs enough USDC.e on Polygon and POL for gas to complete the transaction.

## Withdraw

Withdraw pUSD from the deposit wallet to the owner EOA (default) or a specified address.

```bash
mm predict withdraw --amount <AMOUNT> --wait
mm predict withdraw --amount <AMOUNT> --to <RECIPIENT_ADDRESS> --wait
```

Confirm the amount and recipient with the user before executing. The CLI validates the amount against the on-chain deposit wallet balance before signing.
