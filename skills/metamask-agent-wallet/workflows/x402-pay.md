# Pay an HTTP 402 (x402) paywall

Use when an HTTP request returns `402 Payment Required` (x402), or the user asks to fetch or
pay for a paywalled API, endpoint, file, or resource over HTTP. Autonomous auto-pay is
unsupported — every payment needs explicit user approval. Command details: references/x402.md.

## Preconditions

1. `mm doctor` reports `authenticated: true` and `initialized: true`. If not: SKILL.md § Preflight.
2. `$SKILL_DIR` resolved (references/concepts.md) — the script must be called by absolute path.
3. The URL is `https://` (loopback-only exception for local testing). If http: stop, ask the user.
4. BYOK with an encrypted mnemonic: `MM_PASSWORD` is set (references/concepts.md).
5. Never pass `--toon`/`--format` to the script; it always prints JSON.

## Steps

### 1. Inspect the resource (read-only, no spending)

```bash
python3 "$SKILL_DIR/scripts/x402_pay.py" inspect https://api.example.com/premium
```

For a non-GET resource add `--method POST --data '{"query":"eth"}'`.
Expected output: `{"status": "payment_required", "options": [...]}` on stdout.
Capture: from the option with `"eligible": true` → `asset`, `humanAmount` (or atomic `amount`),
`network`, `payTo`.

### 2. Validate the eligible option

If/then checklist — stop and tell the user if any check fails:

- `eligible` is `true` for at least one option; else see Decision points.
- `payTo` and `asset` match the legend `<address>` format (full 40 hex; no `...`).
- `scheme` is `exact` — the signed amount is exactly `amount`, not a maximum.
- `humanAmount` present → sanity-check it is a plausible price; absent → warn the user the
  amount is shown in raw atomic units.

### 3. Confirm with the user

Show: asset (symbol + contract), amount, network, `payTo`, resource URL. State that a signature
authorizes a real token debit. Do not continue until the user explicitly approves.

### 4. Pay (one attempt only)

```bash
python3 "$SKILL_DIR/scripts/x402_pay.py" pay https://api.example.com/premium --confirm
```

Reuse the exact `--method`/`--data` from step 1. If step 1 showed multiple eligible options, add
`--asset <address>` or `--network <network>` for the one the user chose.
Expected output: `{"status": "settled", "transaction": "0x...", "resource": ...}` on stdout
(exit 0). On exit 1, stderr carries `{"status": "error", "error": ...}`.
Capture: `transaction` → report to the user; `resource` → the paid content.

### 5. Verify and report

If `status` is `settled`: report asset, amount, network, `payTo`, `transaction` (may be `null`
if the server sent no receipt), and return the `resource` body to the user. Anything else:
Decision points below — do NOT rerun `pay`.

## Decision points

- No eligible option / `permit2` / `not a standard x402 challenge` → unsupported paywall; show
  the offered options to the user and stop.
- `multiple eligible options` error at step 4 → ask the user to pick, rerun step 4 once with
  `--asset` or `--network`.
- Error mentions a redirect or `expected HTTP 402, got 3xx` → unexpected redirect; the script
  never follows redirects on payment. Stop and show the user the target — do not pay it.
- `expected HTTP 402, got 200` → resource is free or already paid; just return it.
- `payment not accepted (HTTP <n>)` → surface verbatim and STOP. Never rerun `pay` — the debit
  may already have settled; a rerun signs a new payment. Only retry with fresh user approval.
- User rejects at step 3 → stop. Do not pay.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| `refusing to pay without --confirm` | Complete steps 1–3, then rerun step 4 with `--confirm` |
| `resource URL must be https://` | Ask the user for an https URL |
| `signing failed` | `mm doctor`; BYOK: set `MM_PASSWORD`; references/signing.md |
| `mm produced no JSON` | `mm doctor`; workflows/troubleshooting.md |
| Full table | references/x402.md § Errors |
