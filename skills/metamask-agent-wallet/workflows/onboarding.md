# Onboarding Workflow

Use this workflow when the user is setting up the MetaMask Agentic CLI for the first time.

Reference command syntax in `references/auth.md` and `references/wallet.md`.

## Flow

1. Check CLI installation.
2. Configure environment (if not using production).
3. Login.
4. Initialize wallet mode.
5. Verify auth status.
6. Show wallet address.

## Check CLI Installation

```bash
mm --version
```

If this fails, the CLI is not installed. Guide the user to install it with `npm install -g @metamask/agentic-cli@latest` before proceeding.

Then run the version compatibility check from the skill `Preflight` section: compare the installed `major.minor` against the pinned `cliVersion` and the latest published release, and warn the user if they are out of sync.

## Configure Environment

Production (`prod`) is the default. Set the target environment **before** login if the user needs dev or uat:

```bash
mm config get env
mm config set env dev
```

For a one-off override without persisting, use `MM_ENV=dev mm login` (or `uat`).

To switch environments after a prior login, run `mm logout` or `mm reset` first, then `mm config set env`.

## Login Flow

Ask the user which login method they want to use: MetaMask Mobile QR, Google, or Email. QR (`mm login qr`) is available on non-production builds (dev/uat); on production it returns `COMING_SOON`, so fall back to Google or email there.

### Login

```bash
mm login google --no-wait
mm login email --no-wait
```

Use `--no-wait` for non-interactive environments. The command prints a sign-in URL.

### Verify

Once the user completes sign-in, verify with:

```bash
mm login --token "<TOKEN>"
```

## Initialize Project

First check if the project is already initialized:

```bash
mm init show
```

If already initialized, skip this step.

For server-wallet mode, if the account already has a remote wallet, `mm init` syncs it and reuses the existing trading mode — no trading-mode prompt.

Otherwise, ask the user which wallet mode they want:
- `server-wallet` (recommended) — keys are hosted by MetaMask infrastructure. No need to manage private keys or mnemonics.
- `byok` — bring your own mnemonic. The user manages their own keys locally.

Ask the user which trading mode they want (server-wallet only):
- `guard` — enforces outflow and whitelist policies. When a policy is violated, the CLI requires MFA confirmation before proceeding.
- `beast` — skips all policy checks and confirmations. Useful for scripting or experienced users who want faster execution.

Server wallet:

```bash
mm init --wallet server-wallet --mode guard
```

BYOK:

Never pass `--mnemonic` or `--password` as inline flags. Always instruct the user to set environment variables instead.

```bash
export MM_MNEMONIC="word1 word2 ..."
mm init --wallet byok
```

If the user wants to encrypt their mnemonic with a password during init:

```bash
export MM_MNEMONIC="word1 word2 ..."
export MM_PASSWORD="mypassword"
mm init --wallet byok
```

If the mnemonic was stored unencrypted, suggest setting a password afterward:

```bash
mm wallet password set
```

Once the mnemonic is encrypted, all subsequent operations that need the private key require the `MM_PASSWORD` environment variable to be set. Never instruct the user to pass `--password` inline.

## Verify Auth Status

```bash
mm auth status
```

Confirm the session is authenticated, the wallet mode is correct, and the token is valid.

## Show Wallet Address

```bash
mm wallet address
```
