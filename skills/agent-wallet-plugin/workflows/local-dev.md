# Local development loop

Use this how-to after the package exists, whether from the template or an existing
plugin.

## Enable beta

```bash
mm config set experimentalPlugins true
mm config set experimentalAllowUnverifiedInstalls true
```

Ask before you change the user's config if they did not request it.

## Iterate

```bash
npm run build
mm plugins uninstall PACKAGE_NAME
mm plugins install "file:$PWD" --accept-permissions
mm hello ping Alice --json
```

Skip uninstall if the package is not installed yet.
Replace `PACKAGE_NAME` with the `name` field in `package.json`.
Replace `hello ping` with the command under test.
Use `--accept-permissions` in non-TTY agent sessions.

Install from the directory with `file:$PWD` during development.
Do not use a `.tgz` for local iteration.

## Verify

`mm plugins` lists the package.

`mm help` or `mm TOPIC --help` shows the command.

`--json`, `--toon`, and `--verbose` work without being declared in the plugin.

## Clean up between identity changes

If you rename `package.json` `name`, uninstall the old name.
If you change command ids or capabilities, uninstall and reinstall so consent matches
the new manifest.

## Host CLI version

`mm --version` must satisfy `mm.minCliVersion`.
The template uses `^6.2.0`.
