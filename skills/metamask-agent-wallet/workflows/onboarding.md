# First-time setup (onboarding)

Use when the user has never used the `mm` CLI in this project, or `mm doctor` reports
`authenticated: false` or `initialized: false`. Already authenticated but not initialized:
skip to step 4. Command details: references/auth.md, references/doctor.md.

## Preconditions

1. CLI installed: `mm --version` prints a version. If it fails: `npm install -g @metamask/agentic-cli@latest`.
2. Version check per SKILL.md § Preflight (warn on `major.minor` mismatch, then continue).

## Steps

### 1. Check current state

```bash
mm doctor --toon
```

Expected output: `authenticated` and `initialized` booleans plus `hints`.
Capture: `authenticated` → decides step 2; `initialized` → decides step 4.

### 2. Choose a login method (skip if `authenticated: true`)

Ask the user: MetaMask Mobile QR or browser (Google/Email)? Both work on all environments,
including production.

- QR and interactive terminal available → `mm login qr`
- Otherwise (or user prefers browser) → `mm login browser --no-wait`

### 3. Log in

```bash
mm login browser --no-wait --toon
```

Expected output: a sign-in URL. The user opens it and completes Google or Email sign-in.
If `--no-wait` was used, complete the session: `mm login --token <cli-token> --toon`.

### 4. Choose wallet mode and trading mode (skip if `initialized: true`)

Ask the user:

- Wallet mode: `server-wallet` (recommended; MetaMask hosts the keys) or `byok` (user's own mnemonic).
- Trading mode: `guard` (policy checks enforced) or `beast` (skips policy checks; still blocks malicious transactions).

Confirm both choices explicitly before running init.

### 5. Initialize

If server-wallet:

```bash
mm init --wallet server-wallet --mode guard --toon
```

If BYOK: instruct the user to set env vars (never inline flags), then run:

```bash
export MM_MNEMONIC="word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12"
export MM_PASSWORD="chosen-password"
mm init --wallet byok --mode guard --toon
```

Expected output: `ok: true`. `MM_PASSWORD` is optional here; without it the mnemonic is stored
unencrypted — offer `mm wallet password set` (interactive TTY) afterward.

### 6. Verify readiness

```bash
mm doctor --toon
```

Expected output: `authenticated: true` AND `initialized: true`, no blocking hints. Do not run
other commands until both are true. Never use `mm init show` as this check.

### 7. Report the wallet address

```bash
mm wallet address --toon
```

Expected output: the active wallet address. Show it to the user; setup is complete.

## Decision points

- `mm doctor` already all-true → nothing to do; report ready.
- Server-wallet account already has a remote wallet → `mm init` syncs it and reuses the existing trading mode (no prompt).
- After login in server-wallet mode, wallets auto-sync — `mm wallet list` works immediately.
- User declines to share a mnemonic → use `server-wallet`.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| `ALREADY_AUTHENTICATED` at step 3 | Skip to step 4 (or `mm logout` first to switch accounts) |
| `PAIRING_TIMEOUT` / `MWP_CANCELLED` on QR | Re-run `mm login qr`; scan promptly |
| `INVALID_MNEMONIC` at step 5 | Ask the user to re-check `MM_MNEMONIC`; never echo it |
| `NOT_INITIALIZED` after step 5 | Re-run step 5; check step 3 succeeded first |
