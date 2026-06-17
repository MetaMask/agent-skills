# x402 pay workflow (buyer)

Use this when an HTTP request returns `402 Payment Required` (x402), or the user asks to
fetch/pay for a paywalled API, endpoint, file, or resource over HTTP.

`scripts/x402_pay.py` does the payment. Command details are in `references/x402.md`.

## Flow

1. Inspect the resource.
2. Show the payment to the user and get approval.
3. Pay.
4. Report the settlement and return the resource.

## Inspect

```bash
python3 scripts/x402_pay.py inspect <url>
```

Prints the payment requirement(s) as JSON: asset, human-readable amount, network, `payTo`, and
resource. This is read-only and does not spend.

## Confirm

Show the user the asset, amount, network, `payTo`, and resource URL from the inspect output, and
get explicit approval. A signature authorizes a real token debit.

## Pay

```bash
python3 scripts/x402_pay.py pay <url> --confirm
```

Add `--asset <contract>` or `--network <network>` if the `402` offered more than one eligible
option. For a non-GET resource add `--method` (and `--data` for a body); the same request is
replayed with the payment attached. On success the script prints the settlement transaction and
the resource body.

## Edge cases

- `error` with "no eligible option": the server offered no `exact`-scheme payment on a network mm
  supports. Show the offered options to the user.
- `error` with "multiple eligible options": rerun `pay` with `--asset` or `--network`.
- `error` with "payment not accepted": surface it. Do not rerun blindly; rerunning makes a new
  payment.
- `error` with "not a standard x402 challenge": the endpoint returned a 402 in a different payment
  scheme (for example pay-first then send a transaction hash). This skill supports the standard
  x402 exact scheme only. Tell the user it is unsupported rather than trying to pay.
- Encrypted BYOK mnemonic: set `MM_PASSWORD` so signing is non-interactive.
- Unknown network: the network is not in `mm chains list`; confirm the chain is supported.
