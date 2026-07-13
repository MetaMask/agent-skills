# Doctor command

Use `mm doctor` to inspect CLI version, AI skills, environment, and session health. This command does not require authentication or initialization.

## `doctor` command

### Syntax

```bash
mm doctor
```

### Supported flags

This command does not support additional flags beyond output format options.

### Output

| Field | Type | Description |
| --- | --- | --- |
| `cli` | string | Installed CLI version |
| `env` | string | Current environment (`prod`, `dev`, or `uat`) |
| `authenticated` | boolean | Whether the CLI session is valid |
| `initialized` | boolean | Whether you have run `mm init` (wallet mode and trading mode are set for server wallets) |
| `recommendedSkills` | object | Installed MetaMask AI skill status for `metamask-agent-wallet` and `metamask-agent-workflows` |
| `compatible` | boolean or null | Whether the installed CLI version is compatible with the installed skills. `null` if no skills are detected |
| `hints` | string[] | Actionable guidance, for example missing skills, auth issues, init needed, or version mismatch |

### Skill detection

`mm doctor` detects installed skills from the global skills lock file (`~/.agents/.skill-lock.json` or `$XDG_STATE_HOME/skills/.skill-lock.json`). When the lock file exists but contains no MetaMask entries, it falls back to scanning the current project for installed `metamask-agent-wallet` / `metamask-agent-workflows` skills. It parses `SKILL.md` frontmatter for the skill `version` and `cliVersion` metadata, then checks the CLI `major.minor` against the skill `cliVersion` requirement.

### Example

```bash
mm doctor
mm doctor --toon
```

### Notes

- Use as the first step in troubleshooting to check if CLI, auth, init, and skills are healthy.
- Run after a CLI upgrade to verify skill compatibility.
- Use in CI or scripting to confirm environment and session state.
