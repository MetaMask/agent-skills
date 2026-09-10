# Marketplace submission checklist

Plugin package lives in this repository. Complete these steps after merging the plugin manifests and hook.

## Prerequisites

- [ ] Push `MetaMask/agent-skills` with `.claude-plugin/`, `.cursor-plugin/`, `.codex-plugin/`, `.antigravity-plugin/`, `.grok-plugin/`, `.agents/plugins/`, `hooks/`, root `plugin.json`, and updated `README.md`.
- [ ] Confirm plugin slug remains `metamask-agent-wallet` (immutable after listing).
- [ ] Local smoke:
  - `claude --plugin-dir /path/to/agent-skills`
  - Cursor → Customize → Plugins → add local/Git path to this repo
  - `codex plugin marketplace add /path/to/agent-skills` then `codex plugin add metamask-agent-wallet@metamask`
  - `agy plugin install /path/to/agent-skills/.antigravity-plugin` then `agy plugin list`
  - `grok plugin marketplace add /path/to/agent-skills` then `grok plugin install metamask-agent-wallet --trust`
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

## Codex / ChatGPT

1. Validate locally:

   ```bash
   codex plugin marketplace add /path/to/agent-skills
   codex plugin add metamask-agent-wallet@metamask
   ```

   Codex skips plugin hooks until you review and trust the current hook definition. After trusting, start a new session and confirm `~/.metamask/attribution.json` has `installSource: "codex-plugin"`.

2. Remote marketplace (after the repo is public):

   ```bash
   codex plugin marketplace add MetaMask/agent-skills
   codex plugin add metamask-agent-wallet@metamask
   ```

3. Submit the **skills-only** plugin to the universal ChatGPT / Codex directory:
   - https://platform.openai.com/plugins
   - Submission type: **Skills only** (this plugin does not bundle an MCP server)
   - Listing uses `.codex-plugin/plugin.json` plus `assets/logo.svg`

4. Checklist for review: kebab-case `name`, honest `description`, README, `./`-prefixed paths, no committed secrets, hooks documented (session-start runs `mm doctor`, never auto-installs).

## Antigravity CLI (`agy`)

1. Validate locally:

   ```bash
   agy plugin validate /path/to/agent-skills/.antigravity-plugin
   agy plugin install /path/to/agent-skills/.antigravity-plugin
   ```

   Restart `agy` and run `agy plugin list`. Confirm `metamask-agent-wallet` is enabled.

2. Remote install (after the repo is public):

   ```bash
   agy plugin install https://github.com/MetaMask/agent-skills
   ```

3. Checklist for review: kebab-case `name`, slim `plugin.json` (`name` + `description` only), `skills/` present, rules documented, no committed secrets.

## Grok Build

1. Validate locally:

   ```bash
   grok plugin validate /path/to/agent-skills
   grok plugin marketplace add /path/to/agent-skills
   grok plugin install metamask-agent-wallet --trust
   ```

   Grok skips plugin hooks until you trust the plugin. After trusting, start a new session and confirm `~/.metamask/attribution.json` has `installSource: "grok-plugin"`.

2. Remote marketplace (after the repo is public):

   ```bash
   grok plugin marketplace add MetaMask/agent-skills
   grok plugin install metamask-agent-wallet --trust
   ```

3. Submit the plugin to the official Grok Build catalog with a PR against [xai-org/plugin-marketplace](https://github.com/xai-org/plugin-marketplace):
   - Add one remote entry to `.grok-plugin/marketplace.json`
   - Pin a full 40-character lowercase commit `sha` from `MetaMask/agent-skills`
   - Keep `keywords` brand-scoped (`metamask`, `metamask agent wallet`, `mm cli`) — generic terms like `wallet` or `swap` are rejected
   - Run `python3 scripts/generate-plugin-index.py` and `python3 scripts/validate-catalog.py` in that repo
   - Listing uses this repo's skills plus `hooks/hooks.json` / `hooks/grok-hooks.json`

4. Checklist for review: kebab-case `name`, honest `description`, README, official-org source, no committed secrets, hooks documented (session-start runs `mm doctor`, never auto-installs).

## After listing

- Track `cliVersion` / plugin `version` bumps with `@metamask/agent-wallet` major.minor releases (see README “Release coupling”).
- Do not rename the plugin slug; use `displayName` / `interface.displayName` for label changes.
