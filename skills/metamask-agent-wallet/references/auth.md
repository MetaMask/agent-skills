# Authentication Commands

Use these commands to initialize wallet mode, sign in, inspect authentication status, and clear local session state.

## `init` Command

Initialize the project by selecting wallet mode and trading mode. Requires an authenticated session — run `mm login` first.

### Syntax

```bash
mm init [--wallet <mode>] [--mode <mode>] [--mnemonic <phrase>] [--password <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--wallet` | No | Wallet mode: `server-wallet` or `byok` |
| `--mode` | No | Trading mode: `guard` or `beast` (server-wallet only) |
| `--mnemonic` | No | BIP-39 mnemonic phrase for BYOK wallet. Never pass inline — set `MM_MNEMONIC` env var instead. |
| `--password` | No | Password to encrypt the BYOK mnemonic at rest. Never pass inline — set `MM_PASSWORD` env var instead. If omitted in interactive mode, the CLI prompts. If omitted in non-interactive mode, mnemonic is stored unencrypted. |

### Example

```bash
mm init
mm init --wallet server-wallet --mode beast
export MM_MNEMONIC="word1 word2 ..."
mm init --wallet byok

export MM_MNEMONIC="word1 word2 ..."
export MM_PASSWORD="mypassword"
mm init --wallet byok
```

### Note

- In server-wallet mode, if the account already has a remote EVM wallet, `mm init` syncs it and loads the existing trading mode and policies instead of prompting for a new trading mode or creating a wallet.

## `init show` Command

Display the current initialization settings (wallet mode, trading mode, policies).

### Syntax

```bash
mm init show
```

### Supported Flags

This command does not support additional flags beyond output format options.

### Example

```bash
mm init show
```

## `login` Command

Sign in to the CLI. On a TTY, bare `mm login` shows a method picker (MetaMask Mobile QR, Google, or email). QR is recommended but not auto-selected.

### Syntax

```bash
mm login [qr | google | email] [--token <token>] [--timeout <seconds>] [--no-wait]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--token` | No | Pre-minted CLI token in `cliToken:cliRefreshToken` format [env: `MM_CLI_TOKEN`] |
| `--timeout` | No | Seconds to wait for QR or browser callback |
| `--no-wait` | No | Print the sign-in URL and exit without waiting (for non-interactive/CI use). Not supported with QR login. Complete later with `mm login --token` |

### Example

```bash
mm login --no-wait
mm login google --no-wait
mm login email --no-wait
mm login --token "cliToken:cliRefreshToken"
```

### Note

- If already authenticated, the CLI returns `ALREADY_AUTHENTICATED`. Run `mm logout` first, then log in again.
- `mm login qr` (scan with MetaMask Mobile) is available on non-production builds (dev/uat). On production it returns `COMING_SOON`; use Google or email sign-in instead.
- Pairing codes tolerate `-` and whitespace separators (e.g. `608-225` is equivalent to `608225`).
- Use `mm login google --no-wait` or `mm login email --no-wait` for non-interactive/CI flows. Bare `mm login --no-wait` fails without a TTY because no method is selected.
- `--no-wait` is not supported with QR login. Complete authentication later with `mm login --token`.

## `auth status` Command

Show the current authentication status.

### Syntax

```bash
mm auth status [--toon]
```

### Supported Flags

This command does not support additional flags beyond output format options.

### Example

```bash
mm auth status
mm auth status --toon
```

## `logout` Command

Sign out and clear auth credentials plus local init state, wallet selection, and stored BYOK mnemonic.

### Syntax

```bash
mm logout
```

### Supported Flags

This command does not support flags.

### Example

```bash
mm logout
```

## `config get` Command

Show persisted CLI configuration. Does not require authentication.

### Syntax

```bash
mm config get [env|verbose|format]
```

### Supported Keys

| Key | Description |
| --- | --- |
| `env` | Target API environment: `prod`, `dev`, or `uat` (defaults to `prod` when unset) |
| `verbose` | Whether verbose logging is persisted (`true` or `false`) |
| `format` | Default output format: `json`, `text`, `yaml`, `toml`, or `toon` |

Omit the key to return all values.

### Example

```bash
mm config get
mm config get env
```

## `config set` Command

Persist a CLI configuration value in `~/.metamask/config.json`. Does not require authentication.

### Syntax

```bash
mm config set <env|verbose|format> <value>
```

### Supported Keys

| Key | Values |
| --- | --- |
| `env` | `prod`, `dev`, or `uat` |
| `verbose` | `true` or `false` |
| `format` | `json`, `text`, `yaml`, `toml`, or `toon` |

### Overrides

Persisted values can be overridden per invocation without changing `~/.metamask/config.json`:

| Key | Override |
| --- | --- |
| `env` | `MM_ENV` environment variable |
| `verbose` | `--verbose` / `-v` flag |
| `format` | `--format`, `--json`, `--toon`, etc. |

### Example

```bash
mm config set env prod
mm config set env dev
mm config set env uat
mm config set format toon
```

### Note

- Switch environments at any time with `mm config set env <prod|dev|uat>`.
- Non-prod sessions are stored in env-scoped files under `~/.metamask/` (e.g. `session.dev.json`, `session.uat.json`); prod uses `session.json`.

## `reset` Command

Clear the local CLI session entirely, including auth credentials, wallet state, mnemonic, swap quotes, and persisted config.

### Syntax

```bash
mm reset
```

### Supported Flags

This command does not support flags.

### Example

```bash
mm reset
```

## `wallet password set` Command

Set a password to encrypt the BYOK mnemonic at rest. Only available in BYOK mode when the mnemonic is currently unencrypted.

### Syntax

```bash
mm wallet password set [--new <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--new` | No | New password. If omitted, the CLI prompts interactively. |

### Example

```bash
mm wallet password set
mm wallet password set --new "mypassword"
```

## `wallet password change` Command

Change the BYOK mnemonic encryption password. Only available when the mnemonic is currently encrypted.

### Syntax

```bash
mm wallet password change [--current <password>] [--new <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--current` | No | Current password. If omitted, the CLI prompts interactively. |
| `--new` | No | New password. If omitted, the CLI prompts interactively. |

### Example

```bash
mm wallet password change
mm wallet password change --current "oldpassword" --new "newpassword"
```

## `wallet password remove` Command

Remove the BYOK mnemonic encryption password, storing the mnemonic as plaintext. Only available when the mnemonic is currently encrypted.

### Syntax

```bash
mm wallet password remove [--current <password>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--current` | No | Current password. If omitted, the CLI prompts interactively. |

### Example

```bash
mm wallet password remove
mm wallet password remove --current "mypassword"
```

## Wallet Modes

| Mode | Behavior |
| --- | --- |
| `server-wallet` | Keys hosted by MetaMask infrastructure. Signing and transaction operations may return async job handles. |
| `byok` | Bring your own local mnemonic. Operation results are returned immediately. If the mnemonic is encrypted with a password, the CLI requires `--password` or interactive prompt to unlock before any operation that needs the private key. |
