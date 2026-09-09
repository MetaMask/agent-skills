# Add a command to an existing plugin

## Flow

1. Choose the file path. That path is the CLI path.
2. Implement `PluginCommand` with a matching `pluginCommandId`.
3. Register the id in `package.json` under `mm.commands`.
4. Add `oclif.topics` text if you introduced a new topic folder.
5. Set `requiresAuth`, `requiresInit`, and capabilities honestly.
6. Rebuild and reinstall. Follow `workflows/local-dev.md`.

## Checklist

Confirm `src/commands/TOPIC/NAME.ts` default-exports a `PluginCommand` subclass.

Confirm `pluginCommandId` is `topic:name`, or `name` for a top-level file.

Confirm `mm.commands` has an entry with the same `id`, `capabilities`, and
`dataAccess`.

Confirm plugin-wide `mm.capabilities` is still an empty array.

Confirm the package has no `oclif.hooks`.

Confirm inputs use a schema plus `schemaToFlags` and `schemaToArgs`.
Do not redeclare base flags.

Confirm domain errors throw `CommandError`.

Confirm `npm run build` updates `oclif.manifest.json`.

## Auth defaults

Leave `requiresAuth` and `requiresInit` at the default `true` unless the command is
intentionally public, such as the template ping command.
Read-only chain data still needs auth for `publicClient`.
