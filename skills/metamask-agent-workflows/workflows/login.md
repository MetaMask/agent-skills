# Login Workflow

Use this workflow when the user needs to log in to the CLI.

Reference command syntax in `references/auth.md`.

## Flow

1. Ask the user which login method they want: MetaMask Mobile QR or browser (Google / Email).
2. Execute login.
3. Verify with token.

## Login

For non-interactive/CI flows, use `mm login browser --no-wait`:

```bash
mm login browser --no-wait
```

The command prints a sign-in URL. The user opens it in a browser and chooses Google or Email to complete sign-in.

`mm login qr` (scan with MetaMask Mobile) is available on all environments, including production. QR login keeps the CLI attached to the relay, so it does not support `--no-wait`.

## Verify

Once the user completes sign-in, verify with:

```bash
mm login --token "<TOKEN>"
```

## Confirm

```bash
mm auth status
```

## After Login

In server-wallet mode, wallets are automatically synced after a successful login. Run `mm wallet list` to see them — no need to run `mm init` if wallets already exist. If no wallets are synced, run `mm init` to create one.
