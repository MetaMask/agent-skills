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

Present the following sign-in options to the user:

1. Sign in with MetaMask Mobile — Scan the QR code with MetaMask Mobile. The CLI can only access your agent wallet. Approval requests are sent to MetaMask Mobile.
2. Sign in with Google — Approval requests are sent to your email.
3. Sign in with email — Approval requests are sent to your email.

QR login (`mm-dev login qr`) does not support `--no-wait`. If the user selects QR, they must complete the login flow in the browser.

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

If already initialized, skip this step. Otherwise, ask the user to provision an agent wallet:

1. Server wallet — Keys are managed and secured server-side. Agents can't access your main wallet. You can define policy controls like outflow limits and protocol whitelists.
2. Bring your own wallet — Import a seed phrase. Optionally, encrypt on-device with a password. You approve every transaction with your password if encrypted.

If the user selects `server-wallet`, ask them to choose an operating mode:

1. Guard mode — Guardrails keep the agent in check. Human approval (2FA) is required for agent wallet transactions outside your policies.
   - Guardrails:
     - Security check
     - Whitelisted protocols
     - Outflow limit (rolling 24h)
   - Approval required:
     - Malicious transactions
     - Protocols not in whitelist
     - Raising outflow limit

2. Beast mode — For traders who understand the risks. The agent acts on its own, except when a transaction is flagged as malicious.
   - Guardrails:
     - Security check
   - Approval required:
     - Malicious transactions

Server wallet:

```bash
mm-dev init --wallet server-wallet --mode guard
```

BYOK:

Never pass `--mnemonic` or `--password` as inline flags. Always instruct the user to set environment variables instead.

```bash
export MM_MNEMONIC="word1 word2 ..."
mm-dev init --wallet byok
```

If the user wants to encrypt their mnemonic with a password during init:

```bash
export MM_MNEMONIC="word1 word2 ..."
export MM_PASSWORD="mypassword"
mm-dev init --wallet byok
```

If the mnemonic was stored unencrypted, suggest setting a password afterward:

```bash
mm-dev wallet password set
```

Once the mnemonic is encrypted, all subsequent operations that need the private key require the `MM_PASSWORD` environment variable to be set. Never instruct the user to pass `--password` inline.

## Verify Auth Status

```bash
mm-dev auth status
```

Confirm the session is authenticated, the wallet mode is correct, and the token is valid.

## Show Wallet Address

```bash
mm-dev wallet address
```

## Get started

After setup completes, prompt the user with the following next steps:

- To view wallet details, run `wallet address` or `wallet balance`.
- Transfer funds to this wallet address to start trading (skip if you already have a balance).
