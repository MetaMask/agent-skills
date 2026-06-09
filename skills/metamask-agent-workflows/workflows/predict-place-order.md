# Predict place order workflow

Use this workflow to quote and place a prediction market order.

Reference command syntax in `references/predict.md`.

## Flow

1. Inspect the market to get the outcome token ID.
2. Quote the order.
3. Confirm with the user and place.

## Get outcome token ID

If the user hasn't already identified the market, follow `predict-markets.md` to find and inspect it.

```bash
mm predict markets get <MARKET_SLUG_OR_ID> --json
```

Map the user's intended outcome to the correct token ID from the market detail.

## Quote

Preview the order cost and fill before placing:

```bash
mm predict quote \
  --token-id <OUTCOME_TOKEN_ID> \
  --side buy --size 100 --limit-price 0.55
```

Show the user the estimated cost and fill.

## Place

After the user confirms token ID, outcome, side, size, price, and order type:

```bash
mm predict place \
  --token-id <OUTCOME_TOKEN_ID> \
  --side buy --size 100 --price 0.55 \
  --order-type GTC
```

`--order-type` is one of `GTC`, `GTD`, `FOK`, or `FAK`. `--post-only` only applies to GTC/GTD. `--expiration` is unix seconds for GTD.

## Safety notes

- Prices are 0-1 floats. Treat `--price 1` as suspicious unless the user explicitly confirms.
- Trades are signed by the deposit wallet address shown by `mm predict balance`, not necessarily the connected owner EOA.
- Always inspect the market to map the user's intended outcome to the correct token ID.
