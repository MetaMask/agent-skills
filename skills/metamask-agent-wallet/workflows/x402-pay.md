# x402 pay workflow (buyer)

Use this when an HTTP request returns `402 Payment Required` (x402), when a paid MCP tool call
returns an x402 payment-required result, or the user asks to fetch/pay for a paywalled API,
endpoint, file, tool, or resource.

`scripts/x402_pay.py` does the payment. Command details are in `references/x402.md`. Call it by
its full path inside this skill's directory (`$SKILL_DIR` is the folder containing `SKILL.md`), not
a bare `scripts/...`, because the shell working directory is not stable between commands. It is a
script, not an `mm` command, so do not pass `--toon`/`--format`; it always prints JSON.

## Flow

1. Inspect the resource.
2. Show the payment to the user and get approval.
3. Pay.
4. Report the settlement and return the resource.

## Inspect

```bash
python3 "$SKILL_DIR/scripts/x402_pay.py" inspect <url>
```

Prints the payment requirement(s) as JSON: asset, human-readable amount, network, `payTo`, and
resource. This is read-only and does not spend.

## Confirm

Show the user the asset, amount, network, `payTo`, and resource URL from the inspect output, and
get explicit approval. A signature authorizes a real token debit.

## Pay

```bash
python3 "$SKILL_DIR/scripts/x402_pay.py" pay <url> --confirm
```

Add `--asset <contract>` or `--network <network>` if the `402` offered more than one eligible
option. For a non-GET resource add `--method` (and `--data` for a body); the same request is
replayed with the payment attached. On success the script prints the settlement transaction and
the resource body.

## MCP variant (paid MCP tool)

You (the caller) own the MCP session; the script only signs. Flow:

1. Call the tool unpaid over your MCP session. A paid tool returns a result with
   `isError: true` carrying the `PaymentRequired` challenge.
2. Inspect the challenge (read-only, does not spend). Pass the tool-call response, the tool
   result, or the bare `PaymentRequired` object:

   ```bash
   python3 "$SKILL_DIR/scripts/x402_pay.py" mcp-inspect --challenge '<json>'
   ```

   (`--challenge-file <path>`, or `--challenge -` to read stdin, also work for large
   challenges.)
3. Show the user the asset, amount, network, `payTo`, and resource, and get explicit approval.
4. Sign:

   ```bash
   python3 "$SKILL_DIR/scripts/x402_pay.py" mcp-sign --challenge '<json>' --confirm
   ```

   Add `--asset`/`--network` if the challenge offered more than one eligible option.
5. Retry the same tool call with the printed `payment` object placed, as a raw JSON object, in
   the request params' `_meta["x402/payment"]`.
6. Check the response `_meta["x402/payment-response"]`: `success: true` with a `transaction`
   hash means settled — report both. A result with `isError: true` again is a new challenge
   (verification or settlement failed): surface it to the user, do not re-sign automatically.

## Edge cases

- `error` with "no eligible option": the server offered no `exact`-scheme payment on a network mm
  supports. Show the offered options to the user.
- `error` with "multiple eligible options": the server offered the same scheme on several networks
  or assets (e.g. Base and Polygon). Rerun `pay` with `--network` or `--asset` to choose one.
- `error` mentioning "permit2": the only options use the Permit2 transfer method, which this skill
  does not sign (it supports EIP-3009 only). Tell the user it is unsupported.
- `error` with "payment not accepted": surface it. Do not rerun blindly; rerunning makes a new
  payment.
- `error` with "not a standard x402 challenge": the endpoint returned a 402 in a different payment
  scheme (for example pay-first then send a transaction hash). This skill supports the standard
  x402 exact scheme only. Tell the user it is unsupported rather than trying to pay.
- `error` with "not an x402 payment challenge" (MCP): the tool result was an ordinary tool error,
  not a payment request. Handle it as a normal tool failure.
- `error` with "v2 only" (MCP): the tool sent an x402 v1 challenge; the MCP transport is defined
  for v2 only. Tell the user it is unsupported.
- Encrypted BYOK mnemonic: set `MM_PASSWORD` so signing is non-interactive.
- Unknown network: the network is not in `mm chains list`; confirm the chain is supported.
