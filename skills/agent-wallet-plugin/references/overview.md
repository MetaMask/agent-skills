# Plugin system overview

A plugin is an npm package whose `keywords` include `oclif-plugin`.
It adds first-class `mm` commands.
Those commands show up in `mm help` and the REPL after `mm plugins install`.

Start from the official template at
`https://github.com/MetaMask/agent-wallet-plugin-template`.

## Trust model

Plugins run in-process and unsandboxed.
Install-time consent and MetaMask policy on `wallet-submit` are the real boundaries.
Hiding `session`, the CLI token, and the mnemonic store, and gating `publicClient` and
`walletExecutor`, are defense in depth.
A malicious plugin can still import other packages directly.

## Beta

The feature stays off until you run:

```bash
mm config set experimentalPlugins true
```

If the flag is off, plugin commands fail with `PLUGIN_BETA_DISABLED`.

npm installs fail closed if the registry is unreachable.
Local `file:` sources, git sources, and `plugins link` also need:

```bash
mm config set experimentalAllowUnverifiedInstalls true
```

The host never runs lifecycle scripts such as `postinstall`.
Installs set `npm_config_ignore_scripts=true`.

## Where files live

Installed plugin code lives in the oclif data directory.
On macOS that is `~/Library/Application Support/mm/`.
On Linux that is `~/.local/share/mm/`.

Approvals live in `~/.metamask/config.json` under `plugins` keyed by package name.

The CLI symlinks itself into that data directory at
`node_modules/@metamask/agent-wallet` so plugin imports hit the running CLI.

## SDK import

```ts
import { PluginCommand, type CommandIO } from "@metamask/agent-wallet/plugin";
```

`createAppContext` and the raw host `CommandContext` are not published.
Build only against the plugin export.
