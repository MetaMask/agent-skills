# Authentication Commands

Use these commands to initialize wallet mode, sign in, inspect authentication status, and clear local session state.

## `init` Command

Initialize the project by selecting wallet mode and trading mode.

### Syntax

```bash
mm-dev init [--wallet <mode>] [--mode <mode>] [--mnemonic <phrase>]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--wallet` | No | Wallet mode: `server-wallet` or `byok` |
| `--mode` | No | Trading mode: `safe` or `yolo` |
| `--mnemonic` | No | Mnemonic for BYOK wallet [env: `MM_MNEMONIC`] |

### Example

```bash
mm-dev init
mm-dev init --wallet server-wallet --mode yolo
mm-dev init --wallet byok --mnemonic "word1 word2 ..."
```

## `login` Command

Sign in to the CLI. Defaults to QR / browser flow.

### Syntax

```bash
mm-dev login [qr | google | email] [--token <token>] [--timeout <seconds>] [--no-wait]
```

### Supported Flags

| Name | Required | Description |
| --- | --- | --- |
| `--token` | No | Pre-minted CLI token (`cliToken:cliRefreshToken`) [env: `MM_CLI_TOKEN`] |
| `--timeout` | No | How long to wait for QR / browser callback, in seconds |
| `--no-wait` | No | Print sign-in URL and exit; finish later with `mm-dev login --token` |

### Example

```bash
mm-dev login --no-wait
mm-dev login qr
mm-dev login google --no-wait
mm-dev login email --no-wait
mm-dev login --token "cliToken:cliRefreshToken"
```

### Note

Use `--no-wait` for non-interactive mode except QR flow. It prints the sign-in URL and exits immediately; complete authentication later with `mm-dev login --token`.

## `auth status` Command

Show the current authentication status.

### Syntax

```bash
mm-dev auth status [--toon]
```

### Supported Flags

This command does not support additional flags beyond output format options.

### Example

```bash
mm-dev auth status
mm-dev auth status --toon
```

## `logout` Command

Sign out and clear auth credentials while keeping settings.

### Syntax

```bash
mm-dev logout
```

### Supported Flags

This command does not support flags.

### Example

```bash
mm-dev logout
```

## `reset` Command

Clear the local CLI session entirely.

### Syntax

```bash
mm-dev reset
```

### Supported Flags

This command does not support flags.

### Example

```bash
mm-dev reset
```

## Wallet Modes

| Mode | Behavior |
| --- | --- |
| `server-wallet` | Keys hosted by MetaMask infrastructure. Signing and transaction operations may return async job handles. |
| `byok` | Bring your own local mnemonic. Operation results are returned immediately. |
