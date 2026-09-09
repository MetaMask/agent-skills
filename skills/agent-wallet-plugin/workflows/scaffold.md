# Scaffold from the official template

Use this how-to when you create a plugin from scratch.

## Flow

1. Copy the template.
2. Rename the package and command ids.
3. Install dependencies and build.
4. Follow `workflows/local-dev.md` to install into `mm`.

## Copy

Prefer GitHub's template flow:

```bash
gh repo create my-mm-plugin --template MetaMask/agent-wallet-plugin-template --clone
```

Or copy with degit:

```bash
npx degit MetaMask/agent-wallet-plugin-template my-mm-plugin
cd my-mm-plugin
```

The template URL is `https://github.com/MetaMask/agent-wallet-plugin-template`.

Do not hand-roll the `package.json` `oclif` or `mm` blocks.
Copy them, then edit.

## Rename

1. Set `package.json` `name` to a unique plugin name such as `mm-plugin-hello` or a
   scoped name.
2. Update `description`.
3. If the first command stays `hello ping`, leave ids until the user wants a real
   topic. Then rename the file path, `pluginCommandId`, the `mm.commands` id, and
   `oclif.topics` together.
4. Keep `mm.capabilities` as an empty array.
5. Keep `minCliVersion` and the `@metamask/agent-wallet` peer dependency at `^6.2.0`
   unless the user is targeting a newer host.

## Build

```bash
npm install
npm run build
```

Confirm `dist/` and `oclif.manifest.json` exist.
Then follow `workflows/local-dev.md`.
