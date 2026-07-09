# Login

Use when the user needs to sign in (or `mm doctor` reports `authenticated: false`) on an
already-initialized project. Full first-time setup: workflows/onboarding.md.
Command details: references/auth.md.

## Preconditions

1. CLI installed: `mm --version` prints a version. If not: `npm install -g @metamask/agentic-cli@latest`.
2. Not already signed in: `mm auth status --toon` shows `authenticated: false`. If `true`, stop — nothing to do (to switch accounts, `mm logout` first with user approval).

## Steps

### 1. Choose a method

Ask the user: MetaMask Mobile QR or browser (Google/Email)? Both work on all environments,
including production.

- QR and interactive terminal → `mm login qr` (shows a QR; `--no-wait` not supported)
- Browser or non-interactive → `mm login browser --no-wait`

### 2. Log in

```bash
mm login browser --no-wait --toon
```

Expected output: a sign-in URL. The user opens it and completes Google or Email sign-in.
Capture: the token the user receives → `<cli-token>` in step 3.

### 3. Complete the session (only if `--no-wait` was used)

```bash
mm login --token <cli-token> --toon
```

Expected output: `ok: true` with authenticated session. Never log or store the token.

### 4. Verify

```bash
mm doctor --toon
```

Expected output: `authenticated: true`. If `initialized: false`, continue with
workflows/onboarding.md step 4 before running any wallet command.

## Decision points

- Server-wallet mode → login auto-syncs existing wallets; `mm wallet list` works immediately, no re-init needed.
- BYOK mode → no sync on login; if `initialized: false`, run `mm init` (workflows/onboarding.md).
- User cannot open a browser and has MetaMask Mobile → use `mm login qr` in a TTY.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| `ALREADY_AUTHENTICATED` | Already signed in; `mm logout` first only if the user wants to switch accounts |
| `TOKEN_INVALID` | Re-paste the full `cliToken:cliRefreshToken`; re-run step 2 if expired |
| `PAIRING_TIMEOUT` / `PAIRING_EXPIRED` | Re-run `mm login qr`; scan promptly |
| Login succeeds but commands still fail | workflows/troubleshooting.md |
