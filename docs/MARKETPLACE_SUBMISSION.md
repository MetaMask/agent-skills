# Marketplace submission checklist

Plugin package lives in this repository. Complete these steps after merging the plugin manifests and hook.

## Prerequisites

- [ ] Push `MetaMask/agent-skills` with `.claude-plugin/`, `.cursor-plugin/`, `hooks/`, root `plugin.json`, and updated `README.md`.
- [ ] Confirm plugin slug remains `metamask-agent-wallet` (immutable after listing).
- [ ] Local smoke:
  - `claude --plugin-dir /path/to/agent-skills`
  - Cursor → Customize → Plugins → add local/Git path to this repo
  - New session injects MetaMask readiness context; `~/.metamask/attribution.json` is created without email/PII

## Claude Code

1. Validate locally:

   ```bash
   claude plugin validate .
   claude plugin marketplace add MetaMask/agent-skills
   claude plugin install metamask-agent-wallet@metamask
   ```

2. Submit the **public** GitHub repo to the Claude plugin directory:
   - https://platform.claude.com/plugins/submit
   - or https://claude.ai/admin-settings/directory/submissions/plugins/new

3. In-app submission lists the plugin in the **community** marketplace. The CLI plugin-hint protocol (`<claude-code-hint … value="metamask-agent-wallet@claude-plugins-official" />`) only works for Anthropic’s official marketplace.

4. **Action for MetaMask partner contact:** ask Anthropic to list `metamask-agent-wallet` under `claude-plugins-official` so the stretch CLI hint (plan B5) can ship later.

## Cursor

1. Test with `.cursor-plugin/plugin.json` locally (Customize → Plugins).
2. Submit at https://cursor.com/marketplace/publish
3. Checklist for review: unique kebab-case `name`, honest `description`, README, relative paths only, no committed secrets, hooks documented (session-start runs `mm doctor`, never auto-installs).

## After listing

- Track `cliVersion` / plugin `version` bumps with `@metamask/agent-wallet` major.minor releases (see README “Release coupling”).
- Do not rename the plugin slug; use `displayName` / description for label changes (Claude).
