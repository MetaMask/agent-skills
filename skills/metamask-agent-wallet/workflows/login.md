# Login Workflow

Use this workflow when the user needs to log in to the CLI.

Reference command syntax in `references/auth.md`.

## Flow

1. Ask the user which login method they want: MetaMask Mobile QR, Google, or Email.
2. Execute login.
3. Verify with token.

## Login

For non-interactive/CI flows, use Google or email with `--no-wait`:

```bash
mm login google --no-wait
mm login email --no-wait
```

The command prints a sign-in URL.

`mm login qr` (scan with MetaMask Mobile) is available on non-production builds (dev/uat); on production it returns `COMING_SOON`. QR login keeps the CLI attached to the relay, so it does not support `--no-wait`.

## Verify

Once the user completes sign-in, verify with:

```bash
mm login --token "<TOKEN>"
```

## Confirm

```bash
mm auth status
```
