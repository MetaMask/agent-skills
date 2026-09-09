---
name: agent-wallet-plugin
description: Build MetaMask Agent Wallet CLI mm plugins. Covers PluginCommand, package.json mm manifests, capabilities wallet-read wallet-submit network-manage, local file installs, and npm publish. Use when the user asks to create, scaffold, implement, debug, or publish an mm plugin, PluginCommand, oclif plugin for Agent Wallet, or experimentalPlugins. Do not use this skill for built-in mm wallet, swap, or perps commands. Use metamask-agent-wallet for those.
license: MIT
metadata:
  author: metamask
  version: "1.0.0"
  cliVersion: "6.2.0"
  template: "https://github.com/MetaMask/agent-wallet-plugin-template"
---

# Agent Wallet plugin developer skill

Use this skill to author MetaMask Agent Wallet CLI plugins.
A plugin is an npm package that registers extra `mm` commands.
Plugins import `@metamask/agent-wallet/plugin`, extend `PluginCommand`, and declare
permissions in `package.json` under the `mm` key.

If the user wants built-in `mm` wallet, swap, bridge, perps, predict, or earn commands,
use the `metamask-agent-wallet` skill instead.

Always start a new plugin from the official template at
`https://github.com/MetaMask/agent-wallet-plugin-template`.
Do not invent a package layout.

Use the routing table to select the relevant reference file. Plugin APIs and CLI
behavior live in `references/`. Repeatable authoring patterns live in `workflows/`.

## Command Routing

Match the user's intent to a topic and reference file, then read the reference before
writing code or running install commands. If intent spans multiple domains, load them
sequentially in dependency order.

| User Intent                                              | Topic                         | Reference                                       |
| -------------------------------------------------------- | ----------------------------- | ----------------------------------------------- |
| Trust model, beta flags, unsandboxed runtime             | plugin system                 | [overview.md](references/overview.md)           |
| Template layout, rename map, first command               | template                      | [template.md](references/template.md)           |
| `package.json` `oclif` and `mm` manifest                 | manifest                      | [manifest.md](references/manifest.md)           |
| `PluginCommand`, sealed lifecycle, file path to CLI id   | `PluginCommand`               | [command.md](references/command.md)             |
| Capabilities, `dataAccess`, consent, host-only data      | `wallet-read`, `wallet-submit` | [capabilities.md](references/capabilities.md) |
| `this.ctx`, `publicClient`, `walletExecutor`             | plugin context                | [context.md](references/context.md)             |
| Input schema, flags, `io.resolveInputs`                  | inputs                        | [inputs.md](references/inputs.md)               |
| `CommandError`, output flags, `successHint`              | errors                        | [errors.md](references/errors.md)               |
| Enable plugin beta                                       | `mm config set`               | [install.md](references/install.md)             |
| List installed plugins                                   | `mm plugins`                  | [install.md](references/install.md)             |
| Inspect a plugin                                         | `mm plugins inspect`          | [install.md](references/install.md)             |
| Install a plugin from npm                                | `mm plugins install`          | [install.md](references/install.md)             |
| Install a plugin from a local directory                  | `mm plugins install file:`    | [install.md](references/install.md)             |
| Link a local plugin                                      | `mm plugins link`             | [install.md](references/install.md)             |
| Update an installed plugin                               | `mm plugins update`           | [install.md](references/install.md)             |
| Uninstall a plugin                                       | `mm plugins uninstall`        | [install.md](references/install.md)             |

## Workflows

Plugin APIs live in `references/`. Repeatable patterns live in `workflows/`. Load a
workflow file when the user's request is a pattern, not a single API lookup.

| Pattern                                      | Workflow                                           |
| -------------------------------------------- | -------------------------------------------------- |
| Scaffold from the GitHub template            | [scaffold.md](workflows/scaffold.md)               |
| Build, local `file:` install, iterate        | [local-dev.md](workflows/local-dev.md)             |
| Add another command to an existing plugin    | [add-command.md](workflows/add-command.md)         |
| On-chain reads with `wallet-read`            | [wallet-read.md](workflows/wallet-read.md)         |
| Sign or submit with `wallet-submit`          | [wallet-submit.md](workflows/wallet-submit.md)     |
| Publish to npm                               | [publish.md](workflows/publish.md)                 |
| Plugin install or runtime failures           | [troubleshooting.md](workflows/troubleshooting.md) |

## Preflight

Run these checks once per session before you install or execute plugin commands.

### Host CLI

Plugins require `@metamask/agent-wallet` 6.2.0 or later.
The template sets `minCliVersion` to `^6.2.0`.
You also need Node.js 22.18 or later.

```bash
mm --version
```

If `mm` is missing, ask the user before you run
`npm install -g @metamask/agent-wallet@latest`.
Do not install the CLI silently.

If the installed major.minor is below 6.2, warn the user and stop plugin work until they
upgrade.
Command syntax in this skill will not match older CLIs.

### Beta flags

The plugin system is off by default.
For local development, run:

```bash
mm config set experimentalPlugins true
mm config set experimentalAllowUnverifiedInstalls true
```

`experimentalAllowUnverifiedInstalls` is required for `file:` sources, git sources, and
`mm plugins link`.
npm installs only need `experimentalPlugins`.

### Choose the right skill

If the user wants to call `mm transfer`, `mm swap`, or `mm login`, use
`metamask-agent-wallet`.

If the user wants to add a new `mm` topic as third party code, use this skill.

## Safety rules

Start from the template.
Do not add `oclif.hooks` or `oclif.plugins` to a plugin package.
The host rejects those installs with `PLUGIN_HOOKS_FORBIDDEN`.

Keep plugin-wide `mm.capabilities` as an empty array.
Declare capabilities on each command.

Never declare the reserved capabilities `mnemonic-read` or `config-write`.
Manifest parse fails if you do.

Never read `ctx.session`, CLI tokens, or the mnemonic store.
Those accessors throw `PERMISSION_DENIED`.

Do not override sealed `PluginCommand` members such as `run`, `beforeExecute`, or the
auth, init, and fees getters.
Set static `requiresAuth` and `requiresInit` instead.

Do not redeclare `--json`, `--format`, `--toon`, or `--verbose`.
The host inherits them.

`pluginCommandId` must equal the command `id` in `package.json` under `mm.commands`.
Use a colon-separated id such as `hello:ping`.

Confirm with the user before any `wallet-submit` test that signs or sends a transaction.

Never log or pass mnemonics, passwords, or auth tokens.
Plugin code must not import host-only internals to bypass gates.

Capability gates are not a sandbox.
Plugins run in-process.
Do not tell the user the gates make a malicious plugin safe.

## Output rules

Route silently.
Do not announce which reference you loaded.

Surface CLI errors verbatim.

Prefer `--json` or `--toon` when you verify plugin command output in headless sessions.

After code changes, rebuild with `npm run build` before you reinstall.
Stale `dist/` and `oclif.manifest.json` often look like a runtime bug.
