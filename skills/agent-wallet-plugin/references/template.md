# Official template

The template repository is `https://github.com/MetaMask/agent-wallet-plugin-template`.

It ships one working command:

```bash
mm hello ping
```

You can also pass an optional name argument.

## Layout

```text
package.json
tsconfig.json
src/commands/hello/ping.ts
oclif.manifest.json
```

`package.json` holds the package name, the `oclif` block, the `mm` manifest, and
peer dependencies.

`tsconfig.json` must set `moduleResolution` to `Bundler`.

`oclif.manifest.json` is generated on build and must ship in the npm tarball.

## Rename before you implement product commands

Change `package.json` `name` to a unique npm name such as `mm-plugin-hello` or a scoped
name.

Change `package.json` `description` to an honest one-liner.

Change each `mm.commands` `id` so it matches `pluginCommandId` in source.

Change `oclif.topics` to match your topic help text.

The file path defines the CLI.
`src/commands/hello/ping.ts` becomes `mm hello ping` with id `hello:ping`.
`src/commands/x402.ts` becomes `mm x402` with id `x402`.

## Pins to copy unless the user needs otherwise

The current template uses `mm.schemaVersion` of 1.

It sets `mm.minCliVersion` to `^6.2.0`.

It sets `peerDependencies` for `@metamask/agent-wallet` to `^6.2.0`.

`devDependencies` include `@metamask/agent-wallet`, `oclif`, and `typescript`.

The package `"type"` is `"module"`.

`"files"` lists `dist` and `oclif.manifest.json`.

The `build` script is `tsc -p tsconfig.json && oclif manifest`.

## TypeScript

Host plugin types need `"moduleResolution": "Bundler"`.
Do not switch to `node` or `node10` until you confirm
`@metamask/agent-wallet/plugin` still type-checks.
