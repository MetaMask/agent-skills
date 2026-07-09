# Troubleshooting

Use when a command fails, hangs, prompts unexpectedly, or returns an unknown error.
Error code meanings: references/errors.md. Command details: references/doctor.md.

## Preconditions

1. CLI reachable: `mm --version` prints a version. If `mm: command not found`: `npm install -g @metamask/agentic-cli@latest` and check `PATH`.

## Steps

### 1. Triage with doctor

```bash
mm doctor --toon
```

Expected output: `cli`, `env`, `authenticated`, `initialized`, `hints`.

### 2. Branch on the doctor output

- If `authenticated: false` → workflows/login.md. Fix auth before anything downstream.
- If `initialized: false` → workflows/onboarding.md (step 4).
- If `hints` is non-empty → follow each hint verbatim first.
- If `env` is not what the user expects → `mm config set env prod` (or `dev`/`uat`) after user approval.
- If all healthy → step 3.

### 3. Check the failing command's contract

```bash
mm transfer --help
```

(Substitute the failing command.) Trust the `flags` list over the `usage` string — some usage
strings are wrong (e.g. `wallet trading-mode` prints `mm mode ...`, which does not exist).

### 4. Match the error code

- `NOT_INITIALIZED` → workflows/onboarding.md.
- `AUTH_ERROR` / `TOKEN_REFRESH_FAILED` → workflows/login.md.
- `MNEMONIC_LOCKED` / `WRONG_PASSWORD` → set the correct `MM_PASSWORD` env var, retry.
- `ALREADY_ENCRYPTED` on `wallet password set` → use `mm wallet password change`.
- `NOT_ENCRYPTED` on `wallet password change|remove` → use `mm wallet password set`.
- `CHAIN_ID_MISMATCH` → align payload `domain.chainId` with `--chain-id`.
- Command returned a `pollingId` and seems stuck → `mm wallet requests list --toon`, then `mm wallet requests watch --polling-id <polling-id>` (references/wallet-requests.md).
- `NO_TTY` → pass explicit subcommands/flags (`mm login browser`, `--yes` after approval); password prompts need a real terminal.
- `NETWORK_UNREACHABLE` → check connectivity, retry.
- Anything else → look it up in references/errors.md and surface the CLI message + hint verbatim.

### 5. If the command hangs or hides progress, re-run with debug logs

```bash
mm wallet balance --toon --verbose
```

Expected output: progress/debug lines on stderr; the result stays on stdout.

### 6. Last resort: reset

Only after steps 1-5 fail, and ONLY with the user's explicit confirmation of the scope
("wipes the entire local CLI session; login + init required again"):

```bash
mm reset --yes --toon
```

Expected output: `ok: true`. Then follow workflows/onboarding.md.

## Decision points

- Version mismatch warning in preflight → suggest `npm install -g @metamask/agentic-cli@latest`, then `npx skills add metamask/agent-skills`.
- Error text is clear and user-fixable (bad address, insufficient balance) → relay it verbatim; do not reset.
- User declines the reset confirmation → stop; report remaining state.

## Errors

| Error / symptom | Recovery |
| --- | --- |
| `RESET_FAILED` | Retry `mm reset`; check `~/.metamask/` file permissions |
| Auth worked before, fails now | Token expired: workflows/login.md |
| Unknown flag rejected despite appearing in `usage` | Usage strings can be wrong; trust `flags` list and the reference file |
