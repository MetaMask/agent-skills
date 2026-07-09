# mm auth / login / init / config

Sign in and out, initialize wallet + trading mode, and manage CLI configuration and the BYOK password.

## Prerequisites

- `mm doctor` runs without auth — use it first (references/doctor.md).
- `mm login`, `mm logout`, `mm reset`, `mm config get|set` need no prior auth. `mm init` requires an authenticated session.
- Canonical login is always an explicit subcommand (`mm login browser`, `mm login qr`). Bare `mm login` opens a TTY-only method picker and fails without a TTY — never use it from a script or agent.
- Secrets travel only via `MM_MNEMONIC` (read ONLY by `mm init`) and `MM_PASSWORD` — never as flags (references/concepts.md).

## mm auth status

Show whether the CLI session is authenticated and how. Read-only.

### Syntax

```bash
mm auth status
```

No non-global flags. Global flags apply — see SKILL.md § Global flags.

### Output

```
ok: true
data:
  authenticated: true
  summary:
    mode: session
    signedInAs: BFr2FRheqx_PUMcyhj6…
    method: Stored session
```

## mm login browser

Sign in via the browser (Google or Email — the user picks in the browser). State-changing (local session only; no wallet job).

### Syntax

```bash
mm login browser [--no-wait]
```

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--no-wait` | off | boolean flag | Print the sign-in URL and exit without waiting. Complete later with `mm login --token` (below). |
| `--timeout` | CLI default | integer seconds | Seconds to wait for the browser callback |

Global flags apply — see SKILL.md § Global flags.

### Examples

```bash
mm login browser --no-wait --toon
```

If `--no-wait` was used, after the user finishes in the browser complete the session with the token they receive:

```bash
mm login --token <cli-token> --toon
```

`--token` takes a pre-minted CLI token in `cliToken:cliRefreshToken` format (env: `MM_CLI_TOKEN`). Never log it.

## mm login qr

Sign in by scanning a QR code with MetaMask Mobile. Works on ALL environments, including production. State-changing (local session only). Requires an interactive terminal to display the QR; `--no-wait` is NOT supported.

### Syntax

```bash
mm login qr
```

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--timeout` | CLI default | integer seconds | Seconds to wait for the mobile pairing |

Global flags apply — see SKILL.md § Global flags. Pairing codes tolerate `-` and whitespace (`608-225` = `608225`).

## mm logout

Sign out: clears auth credentials plus local init state. State-changing (local session only).

### Syntax

```bash
mm logout [--yes]
```

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--yes` | off | boolean flag | Skip the confirmation prompt (non-interactive use) |

Global flags apply — see SKILL.md § Global flags.

### Confirm before executing

Show the user: "Sign out and clear the local session (auth credentials and init state)?" Only after explicit approval, run:

```bash
mm logout --yes --toon
```

## mm reset

Clear the local CLI session entirely (logout plus wipe saved credentials). Destructive — last-resort troubleshooting only (workflows/troubleshooting.md).

### Syntax

```bash
mm reset [--yes]
```

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--yes` | off | boolean flag | Skip the confirmation prompt (non-interactive use) |

Global flags apply — see SKILL.md § Global flags.

### Confirm before executing

Show the user the exact scope: "Reset wipes the entire local CLI session — you will need to log in and run `mm init` again." Require explicit approval (SKILL.md § Safety invariants). Only then run:

```bash
mm reset --yes --toon
```

## mm init

Initialize the project: choose wallet mode (`server-wallet` or `byok`) and trading mode (`guard` or `beast`). Requires an authenticated session. State-changing (local + server-side registration; no on-chain write).

Choose the sub-block by wallet mode. If the user has their own mnemonic → BYOK; otherwise → server-wallet (recommended).

### Server-wallet

```bash
mm init --wallet server-wallet --mode guard
```

If the account already has a remote EVM wallet, `mm init` syncs it and reuses the existing trading mode instead of prompting or creating a new wallet.

### BYOK

```bash
export MM_MNEMONIC="word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12"
mm init --wallet byok --mode guard
```

To encrypt the mnemonic at rest, also `export MM_PASSWORD` before running. Without it in non-interactive mode the mnemonic is stored unencrypted — offer `mm wallet password set` afterward. `MM_MNEMONIC` is read ONLY by `mm init`.

### Optional flags

| Flag | Default | Value format | Description |
| --- | --- | --- | --- |
| `--wallet` | interactive prompt | `server-wallet` or `byok` | Wallet mode |
| `--mode` | interactive prompt / server value | `guard` or `beast` | Trading mode (references/concepts.md § Trading modes) |

Global flags apply — see SKILL.md § Global flags. BYOK with an encrypted mnemonic: set
`MM_PASSWORD` first (references/concepts.md). The CLI also accepts `--mnemonic`/`--password`; NEVER use them — set `MM_MNEMONIC`/`MM_PASSWORD` instead.

### Confirm before executing

Show the user: wallet mode, trading mode, and (BYOK) whether the mnemonic will be password-encrypted. Wait for approval.

## mm init show

Show current init settings (wallet mode, trading mode). Read-only. Throws `NOT_INITIALIZED` on an uninitialized project — never use it as a readiness check; use `mm doctor` (references/doctor.md).

### Syntax

```bash
mm init show
```

No non-global flags. Global flags apply — see SKILL.md § Global flags.

## mm config get

Show persisted CLI configuration (`~/.metamask/config.json`). Read-only. No auth required.

### Syntax

```bash
mm config get [<key>]
```

`<key>` is one of `env`, `verbose`, `format`, `walletTimeoutSeconds`. Omit it to show all values. No non-global flags. Global flags apply — see SKILL.md § Global flags.

### Examples

```bash
mm config get env --toon
```

## mm config set

Persist a CLI configuration value. State-changing (local file only). Positional-only — there are no key/value flags.

### Syntax

```bash
mm config set <key> <value>
```

| Key | Values | Per-invocation override |
| --- | --- | --- |
| `env` | `prod`, `dev`, `uat` | `MM_ENV` env var |
| `verbose` | `true`, `false` | `--verbose` |
| `format` | `text`, `json`, `toon` | `--format` / `--json` / `--toon` |
| `walletTimeoutSeconds` | integer ≤ 600 | `--wallet-timeout` |

Global flags apply — see SKILL.md § Global flags. Non-prod sessions live in env-scoped files under `~/.metamask/` (`session.dev.json`, `session.uat.json`); prod uses `session.json`.

### Examples

```bash
mm config set walletTimeoutSeconds 300 --toon
```

## mm wallet password set | change | remove

Manage the password encrypting the BYOK mnemonic at rest. State-changing (local file only). ALWAYS run these in an interactive TTY and let the CLI prompt — never pass `--new` or `--current` inline (they exist but would leak the secret into shell history).

If the mnemonic is unencrypted → `set`. If already encrypted → `change` or `remove`.

### Syntax

```bash
mm wallet password set
mm wallet password change
mm wallet password remove
```

Global flags apply — see SKILL.md § Global flags. After encryption, every signing command needs `MM_PASSWORD` set (references/concepts.md).

## Errors

| Code | Cause | Recovery |
| --- | --- | --- |
| `ALREADY_AUTHENTICATED` | `mm login` while a valid session exists | Run `mm logout` first, then log in again |
| `AUTH_FAILED` / `TOKEN_INVALID` | Sign-in or token verification failed | Retry `mm login browser`; check the token was pasted whole |
| `PAIRING_TIMEOUT` / `PAIRING_EXPIRED` / `MWP_TIMEOUT` / `MWP_CANCELLED` | QR pairing timed out or was cancelled on mobile | Re-run `mm login qr` and scan promptly |
| `NO_TTY` | Bare `mm login`, or a password prompt, without a terminal | Use `mm login browser --no-wait`; run password commands in a TTY |
| `NOT_INITIALIZED` | `mm init show` (or another command) before `mm init` | Follow workflows/onboarding.md |
| `INVALID_MNEMONIC` | Bad BIP-39 phrase in `MM_MNEMONIC` | Ask the user to re-check the phrase; never echo it |
| `INVALID_CONFIG_KEY` / `INVALID_CONFIG_VALUE` | Unknown config key or bad value | Use only the keys/values in the `mm config set` table |
| `ALREADY_ENCRYPTED` | `password set` on an encrypted mnemonic | Use `mm wallet password change` |
| `NOT_ENCRYPTED` | `password change`/`remove` on an unencrypted mnemonic | Use `mm wallet password set` |
| `WRONG_PASSWORD` | Wrong current password | Re-prompt the user interactively |

Full code list: references/errors.md.
