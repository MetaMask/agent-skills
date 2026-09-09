# Errors and output

## Failures

Throw `CommandError`.
Do not return a handmade `CommandResult` for the happy path.
Return plain data from `execute`.
The host wraps it.

```ts
import { CommandError } from "@metamask/agent-wallet/plugin";

throw new CommandError(
  "ENS_NAME_NOT_FOUND",
  `'${name}' does not resolve to an address.`,
  "Check the spelling of the name."
);
```

The constructor takes `code`, `message`, and `hint`, all strings.
Use a stable code such as `ENS_NAME_NOT_FOUND`.
Surface host errors to the user verbatim when they come from `mm` itself.

## Host plugin codes

`PLUGIN_BETA_DISABLED` means `experimentalPlugins` is false.

`PLUGIN_SEALED_OVERRIDE` means a subclass overrode a sealed lifecycle member.

`PLUGIN_HOOKS_FORBIDDEN` means the package declared `oclif.hooks` or `oclif.plugins`.

`PLUGIN_CLI_VERSION` means `minCliVersion` is not satisfied.

`PLUGIN_MANIFEST_FILE_MISSING` means the installed package has no `oclif.manifest.json`.

`PERMISSION_DENIED` means a missing capability or a host-only resource.

`MISSING_FLAG` means a required input is missing in headless mode.

## Success

Return a serializable object.
Optional `successHint` adds a one-line human hint.

## Formats

The host inherits `--format` with `text`, `json`, or `toon`, plus `--json`, `--toon`,
and `--verbose`.

The last format token on argv wins.
Piped output and `--json` are headless and have no prompts.
Use `io.notify` for structured notices such as MFA or transaction steps.
Those appear as `_notice` objects in JSON.
