# Plugin troubleshooting

Always rebuild before you reinstall.

Then run:

```bash
mm --version
mm plugins
mm plugins inspect PACKAGE_NAME
mm COMMAND --help
```

Replace `PACKAGE_NAME` and `COMMAND` with the plugin and command under test.

## PLUGIN_BETA_DISABLED

The beta flag is off.
Run `mm config set experimentalPlugins true`.

## Local file install refused

Unverified sources are blocked.
Run `mm config set experimentalAllowUnverifiedInstalls true`.

## Bare path treated as a GitHub slug

The spec is missing the `file:` prefix.
Run `mm plugins install "file:$PWD"`.

## PLUGIN_MANIFEST_FILE_MISSING

The package did not ship or generate `oclif.manifest.json`.
Run `npm run build` and include `oclif.manifest.json` in `files`.

## PLUGIN_HOOKS_FORBIDDEN

The package declared `oclif.hooks` or `oclif.plugins`.
Remove them.

## PLUGIN_CLI_VERSION

The host is older than `minCliVersion`.
Upgrade `@metamask/agent-wallet`.

## PLUGIN_SEALED_OVERRIDE

The subclass overrode a sealed lifecycle member.
Implement only `execute` and the allowed hooks.
Use static auth and init fields.

## Command missing from mm help

The id is missing from `mm.commands`, the build is stale, or the id collides with a
built-in command.
Rebuild, match `pluginCommandId`, and pick a unique topic.

## PERMISSION_DENIED on publicClient or reads

The command lacks `wallet-read`, or consent is stale.
Add the capability, then uninstall and reinstall.

## PERMISSION_DENIED on walletExecutor

The command lacks `wallet-submit`, or consent is stale.
Add the capability, then uninstall and reinstall.

## PERMISSION_DENIED on session or mnemonic

Those resources are host-only.
Use `walletStateManager` and `walletExecutor`.

## Gated APIs fail after a manifest edit

`manifestHash` no longer matches the approval.
Uninstall, then install again from `file:$PWD`.

## MISSING_FLAG in CI

The field only prompts and there is no TTY.
Pass flags or positionals and set `prompt: false`.

## Types fail on the plugin export

`moduleResolution` is wrong.
Set `"Bundler"` in `tsconfig.json`.

## Two copies of the CLI at runtime

The plugin bundled the host instead of using a peer dependency.
Keep a peer dependency only and rely on the host symlink.
