# Onboarding Workflow

Use this workflow when the user is setting up the MetaMask Agentic CLI for the first time.

Reference command syntax in `references/auth.md` and `references/wallet.md`.

## Flow

1. Check CLI installation.
2. Login.
3. Initialize wallet mode.
4. Verify auth status.
5. Show wallet address.

## Check CLI Installation

```bash
mm-dev --version
```

If this fails, the CLI is not installed. Guide the user to install it before proceeding.

## Login Flow

Ask the user which login method they want to use: Google, Email, or QR.
QR login (`mm-dev login qr`) does not support `--no-wait`. If the user wants QR, they must complete the onboarding flow themselves.

### Login

```bash
mm-dev login google --no-wait
mm-dev login email --no-wait
```

Use `--no-wait` for non-interactive environments. The command prints a sign-in URL.

### Verify

Once the user completes sign-in, verify with:

```bash
mm-dev login --token "<TOKEN>"
```

## Initialize Project

First check if the project is already initialized:

```bash
mm-dev init show
```

If already initialized, skip this step. Otherwise, ask the user which wallet mode they want:
- `server-wallet` (recommended) — keys are hosted by MetaMask infrastructure. No need to manage private keys or mnemonics.
- `byok` — bring your own mnemonic. The user manages their own keys locally.

Ask the user which trading mode they want:
- `safe` — enforces outflow and whitelist policies. When a policy is violated, the CLI requires MFA confirmation before proceeding.
- `yolo` — skips all policy checks and confirmations. Useful for scripting or experienced users who want faster execution.

Server wallet:

```bash
mm-dev init --wallet server-wallet --mode safe
```

BYOK:

```bash
mm-dev init --wallet byok --mnemonic "word1 word2 ..."
```

## Verify Auth Status

```bash
mm-dev auth status
```

Confirm the session is authenticated, the wallet mode is correct, and the token is valid.

## Show Wallet Address

```bash
mm-dev wallet address
```
