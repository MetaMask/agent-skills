# Login Workflow

Use this workflow when the user needs to log in to the CLI.

Reference command syntax in `references/auth.md`.

## Flow

1. Present login options with descriptions.
2. Execute login.
3. Verify with token.

## Login

Present the following sign-in options to the user:

1. Sign in with MetaMask Mobile — Scan the QR code with MetaMask Mobile. The CLI can only access your agent wallet. Approval requests are sent to MetaMask Mobile.
2. Sign in with Google — Approval requests are sent to your email.
3. Sign in with email — Approval requests are sent to your email.

QR login (`mm-dev login qr`) does not support `--no-wait`. If the user selects QR, they must complete the login flow in the browser.

```bash
mm-dev login google --no-wait
mm-dev login email --no-wait
```

Use `--no-wait` for non-interactive environments. The command prints a sign-in URL.

## Verify

Once the user completes sign-in, verify with:

```bash
mm-dev login --token "<TOKEN>"
```

## Confirm

```bash
mm-dev auth status
```
