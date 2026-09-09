# Publish to npm

## Package contents

The tarball must include compiled ESM in `dist/`.

It must include `oclif.manifest.json` generated in `prepack` or `build`.

`"files"` must list `dist` and `oclif.manifest.json`.

`keywords` must include `oclif-plugin`.

`peerDependencies` for `@metamask/agent-wallet` must match `minCliVersion`.

## Preflight

```bash
npm run build
npm pack --dry-run
```

Confirm the tarball contains `oclif.manifest.json` and `dist/commands`.
If the manifest is missing, users get `PLUGIN_MANIFEST_FILE_MISSING` and a rollback.

Do not rely on `postinstall` to build.
The CLI installs with scripts ignored.

## Publish

Follow the user's npm org process, including `npm publish` and provenance.
Users then run:

```bash
mm config set experimentalPlugins true
mm plugins install PACKAGE_NAME
```

Replace `PACKAGE_NAME` with the published package name.

They get a consent screen listing commands, `dataAccess`, and capabilities.

## After publish

Document `minCliVersion`.
If you bump capabilities, existing installs need `mm plugins update` and a new consent.
