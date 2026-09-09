# Install and manage

You must set `experimentalPlugins` to true before install, add, update, link, or reset.
`mm plugins`, `inspect`, and `uninstall` work without the beta flag.

## User install from npm

```bash
mm config set experimentalPlugins true
mm plugins install @scope/mm-my-plugin
```

For CI or a non-TTY session:

```bash
mm plugins install @scope/mm-my-plugin --accept-permissions --json
```

A `--json` install in non-interactive mode requires `--accept-permissions`.

## Local authoring from a directory

Install from the package directory, not a packed tarball, so the CLI can read
`package.json` `mm` for approvals.

```bash
mm config set experimentalPlugins true
mm config set experimentalAllowUnverifiedInstalls true
mm plugins install "file:$PWD" --accept-permissions
```

You can also run `mm plugins link` with the package path.
That path still needs unverified installs and consent.

A bare path without the `file:` prefix is treated as a GitHub slug and is refused.

## Other commands

```bash
mm plugins
mm plugins inspect PACKAGE_NAME
mm plugins update
mm plugins update PACKAGE_NAME
mm plugins uninstall PACKAGE_NAME
mm plugins add
```

`mm plugins` lists installed plugins.

`mm plugins update` asks for consent again if version or manifest changed.

`mm plugins uninstall` drops approval on success.

`mm plugins add` is an alias of install.

## After changing capabilities or command ids

Uninstall, rebuild, and reinstall so `manifestHash` and `approvedCommandIds` match.
Stale approvals yield empty runtime grants and `PERMISSION_DENIED` on gated APIs.
