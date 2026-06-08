# Login Workflow

Use this workflow when the user needs to log in to the CLI.

Reference command syntax in `references/auth.md`.

## Flow

1. Ask the user which login method they want: Google or Email. QR login is coming soon and is not available.
2. Execute login.
3. Verify with token.

## Login

`mm login qr` returns `COMING_SOON`. Use Google or email sign-in.

```bash
mm login google --no-wait
mm login email --no-wait
```

Use `--no-wait` for non-interactive environments. The command prints a sign-in URL.

## Verify

Once the user completes sign-in, verify with:

```bash
mm login --token "<TOKEN>"
```

## Confirm

```bash
mm auth status
```
