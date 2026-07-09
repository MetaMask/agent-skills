# mm doctor

One-shot health check: CLI version, environment, authentication, initialization, and installed MetaMask AI skills. Requires neither auth nor init — it is always the first command to run.

## Prerequisites

- None. `mm doctor` works on a fresh, logged-out install.

## mm doctor

Inspect CLI, skills, environment, and session health. Read-only.

### Syntax

```bash
mm doctor
```

No non-global flags. Global flags apply — see SKILL.md § Global flags.

### Output

```
ok: true
data:
  cli: 4.0.1
  env: prod
  authenticated: true
  initialized: true
  recommendedSkills:
    "metamask-agent-wallet":
      found: false
      name: metamask-agent-wallet
    "metamask-agent-workflows":
      found: false
      name: metamask-agent-workflows
  compatible: null
  hints[1]: No MetaMask AI skills found. Install with `npx skills add metamask/agent-skills`.
```

| Field | Meaning |
| --- | --- |
| `cli` | Installed CLI version |
| `env` | Active environment: `prod`, `dev`, or `uat` |
| `authenticated` | Session is valid. `false` → workflows/login.md |
| `initialized` | `mm init` has been completed. `false` → workflows/onboarding.md |
| `recommendedSkills` | Detected MetaMask AI skills (global lock file, falling back to the project directory) |
| `compatible` | CLI `major.minor` matches the installed skill's pinned `cliVersion`; `null` when no skills detected |
| `hints` | Actionable next steps (missing skills, auth needed, init needed, version mismatch) |

### Gates and readiness

1. If `authenticated: false` → every wallet/trading command will fail with an auth error. Fix first (workflows/login.md).
2. If `initialized: false` → wallet operations fail with `NOT_INITIALIZED`. Fix second (workflows/onboarding.md).
3. Only when BOTH are `true` and no blocking `hints` remain is the session ready.
4. Follow any `hints` verbatim — they are the CLI's own remediation guidance.
5. NEVER use `mm init show` as a readiness check: it throws `NOT_INITIALIZED` on an uninitialized project instead of reporting state. `mm auth status` reports only authentication, not initialization.

### Examples

```bash
mm doctor --toon
```

### Errors

| Code | Cause | Recovery |
| --- | --- | --- |
| `mm: command not found` (shell) | CLI not installed or not on `PATH` | `npm install -g @metamask/agentic-cli@latest`, then re-run |
| `NETWORK_UNREACHABLE` | No network to backend | Check connectivity; retry |

Full code list: references/errors.md.
