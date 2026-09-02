#!/usr/bin/env sh
# Session-start hook for MetaMask Agent Wallet plugin (Claude Code + Cursor).
# Never installs software. Always exits 0. Emits host-specific additional context.
set -eu

HOST=""
while [ $# -gt 0 ]; do
  case "$1" in
    --host)
      HOST="${2:-}"
      shift 2
      ;;
    --host=*)
      HOST="${1#--host=}"
      shift
      ;;
    *)
      shift
      ;;
  esac
done

case "$HOST" in
  claude-code|cursor) ;;
  *) HOST="unknown" ;;
esac

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-${CURSOR_PLUGIN_ROOT:-}}"
if [ -z "$PLUGIN_ROOT" ]; then
  PLUGIN_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
fi

SKILL_MD="$PLUGIN_ROOT/skills/metamask-agent-wallet/SKILL.md"
PLUGIN_VERSION="1.0.0"
CLI_VERSION="6.1.5"
if [ -f "$SKILL_MD" ]; then
  # Prefer metadata.cliVersion / metadata.version from YAML frontmatter.
  extracted_cli=$(sed -n 's/^[[:space:]]*cliVersion:[[:space:]]*"\([^"]*\)".*/\1/p' "$SKILL_MD" | head -n 1)
  extracted_ver=$(sed -n 's/^[[:space:]]*version:[[:space:]]*"\([^"]*\)".*/\1/p' "$SKILL_MD" | head -n 1)
  [ -n "$extracted_cli" ] && CLI_VERSION="$extracted_cli"
  [ -n "$extracted_ver" ] && PLUGIN_VERSION="$extracted_ver"
fi

case "$HOST" in
  claude-code) INSTALL_SOURCE="claude-code-plugin" ;;
  cursor) INSTALL_SOURCE="cursor-plugin" ;;
  *) INSTALL_SOURCE="unknown-plugin" ;;
esac

NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%SZ")
ATTR_DIR="${HOME}/.metamask"
ATTR_FILE="${ATTR_DIR}/attribution.json"

upsert_attribution() {
  mkdir -p "$ATTR_DIR" 2>/dev/null || return 0
  chmod 700 "$ATTR_DIR" 2>/dev/null || true

  if [ -f "$ATTR_FILE" ]; then
    # Update lastSeenAt / pluginVersion in place via node if available; else leave as-is.
    if command -v node >/dev/null 2>&1; then
      INSTALL_SOURCE="$INSTALL_SOURCE" PLUGIN_VERSION="$PLUGIN_VERSION" NOW="$NOW" ATTR_FILE="$ATTR_FILE" node <<'NODE' || true
const fs = require("fs");
const path = process.env.ATTR_FILE;
let data = {};
try {
  data = JSON.parse(fs.readFileSync(path, "utf8"));
} catch {
  data = {};
}
if (typeof data !== "object" || data === null || Array.isArray(data)) data = {};
if (!data.firstSeenAt) data.firstSeenAt = process.env.NOW;
data.lastSeenAt = process.env.NOW;
data.pluginVersion = process.env.PLUGIN_VERSION;
if (!data.installSource) data.installSource = process.env.INSTALL_SOURCE;
fs.writeFileSync(path, JSON.stringify(data, null, 2) + "\n", { mode: 0o600 });
try { fs.chmodSync(path, 0o600); } catch { /* ignore */ }
NODE
    fi
  else
    cat >"$ATTR_FILE" <<EOF
{
  "installSource": "${INSTALL_SOURCE}",
  "pluginVersion": "${PLUGIN_VERSION}",
  "firstSeenAt": "${NOW}",
  "lastSeenAt": "${NOW}"
}
EOF
    chmod 600 "$ATTR_FILE" 2>/dev/null || true
  fi
}

upsert_attribution || true

# Bonus for Claude Code: export plugin env for subsequent Bash tool calls.
if [ "$HOST" = "claude-code" ] && [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  {
    echo "export MM_PLUGIN_HOST=${HOST}"
    echo "export MM_PLUGIN_VERSION=${PLUGIN_VERSION}"
    echo "export MM_PLUGIN_ROOT=${PLUGIN_ROOT}"
  } >>"$CLAUDE_ENV_FILE" 2>/dev/null || true
fi

MAX_CONTEXT=3500
CONTEXT=""

json_escape() {
  # Escape a string for JSON using node when available; fallback strips quotes/newlines.
  if command -v node >/dev/null 2>&1; then
    printf '%s' "$1" | node -e 'let s="";process.stdin.on("data",d=>s+=d);process.stdin.on("end",()=>process.stdout.write(JSON.stringify(s).slice(1,-1)))'
  else
    printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g; s/	/\\t/g' | tr '\n' ' '
  fi
}

if ! command -v mm >/dev/null 2>&1; then
  CONTEXT="MetaMask Agent Wallet CLI is not installed. Before any wallet, swap, bridge, perps, predict, or earn operation, ask the user for permission to run: npm install -g @metamask/agent-wallet@${CLI_VERSION}. After install, run mm doctor and follow its hints (mm login / mm init) before other commands. Plugin version ${PLUGIN_VERSION}; host ${HOST}."
else
  DOCTOR_OUT=""
  DOCTOR_STATUS=0
  # shellcheck disable=SC2039
  if command -v timeout >/dev/null 2>&1; then
    DOCTOR_OUT=$(
      MM_PLUGIN_HOST="$HOST" \
      MM_PLUGIN_ROOT="$PLUGIN_ROOT" \
      MM_PLUGIN_VERSION="$PLUGIN_VERSION" \
      timeout 15 mm doctor --json 2>/dev/null
    ) || DOCTOR_STATUS=$?
  elif command -v gtimeout >/dev/null 2>&1; then
    DOCTOR_OUT=$(
      MM_PLUGIN_HOST="$HOST" \
      MM_PLUGIN_ROOT="$PLUGIN_ROOT" \
      MM_PLUGIN_VERSION="$PLUGIN_VERSION" \
      gtimeout 15 mm doctor --json 2>/dev/null
    ) || DOCTOR_STATUS=$?
  else
    DOCTOR_OUT=$(
      MM_PLUGIN_HOST="$HOST" \
      MM_PLUGIN_ROOT="$PLUGIN_ROOT" \
      MM_PLUGIN_VERSION="$PLUGIN_VERSION" \
      mm doctor --json 2>/dev/null
    ) || DOCTOR_STATUS=$?
  fi

  if [ -z "$DOCTOR_OUT" ] || [ "$DOCTOR_STATUS" -ne 0 ]; then
    CONTEXT="MetaMask Agent Wallet CLI is installed but mm doctor failed or timed out. Run mm doctor yourself and follow its hints before wallet operations. Expected CLI major.minor ${CLI_VERSION}. Plugin version ${PLUGIN_VERSION}; host ${HOST}."
  elif command -v node >/dev/null 2>&1; then
    CONTEXT=$(
      DOCTOR_OUT="$DOCTOR_OUT" CLI_VERSION="$CLI_VERSION" PLUGIN_VERSION="$PLUGIN_VERSION" HOST="$HOST" node <<'NODE'
const raw = process.env.DOCTOR_OUT || "";
let parsed;
try {
  parsed = JSON.parse(raw);
} catch {
  const start = raw.indexOf("{");
  const end = raw.lastIndexOf("}");
  if (start >= 0 && end > start) {
    try { parsed = JSON.parse(raw.slice(start, end + 1)); } catch { parsed = null; }
  }
}
// mm wraps command results as { ok, data } — unwrap when present.
const data =
  parsed && typeof parsed === "object" && parsed.data && typeof parsed.data === "object"
    ? parsed.data
    : parsed;
if (!data || typeof data !== "object") {
  console.log(`MetaMask Agent Wallet: mm doctor returned unparseable output. Run mm doctor manually. Plugin ${process.env.PLUGIN_VERSION}; host ${process.env.HOST}.`);
  process.exit(0);
}
const parts = [];
parts.push(`MetaMask Agent Wallet CLI ${data.cli || "unknown"} (plugin ${process.env.PLUGIN_VERSION}, host ${process.env.HOST}).`);
if (data.compatible === false) {
  const pinned = process.env.CLI_VERSION;
  parts.push(`CLI/skill version mismatch. Ask the user before running: npm install -g @metamask/agent-wallet@${pinned}.`);
}
if (data.authenticated === false) {
  parts.push("Not authenticated. Follow the skill onboarding/login workflow (mm login browser --no-wait, then mm login --token).");
}
if (data.authenticated === true && data.initialized === false) {
  parts.push("Authenticated but not initialized. Run mm init to choose wallet and trading modes.");
}
if (Array.isArray(data.hints) && data.hints.length > 0) {
  parts.push("Doctor hints: " + data.hints.slice(0, 5).join(" | "));
}
if (data.authenticated === true && data.initialized === true && data.compatible !== false) {
  parts.push("Ready: authenticated and initialized. Prefer mm doctor before the first wallet operation in a session.");
}
console.log(parts.join(" "));
NODE
    ) || CONTEXT="MetaMask Agent Wallet: could not summarize mm doctor output. Run mm doctor manually."
  else
    CONTEXT="MetaMask Agent Wallet CLI is installed. Run mm doctor and follow its hints before wallet operations. Expected CLI ${CLI_VERSION}. Plugin ${PLUGIN_VERSION}; host ${HOST}."
  fi
fi

# Hard-cap context length.
CONTEXT_LEN=$(printf '%s' "$CONTEXT" | wc -c | tr -d ' ')
if [ "$CONTEXT_LEN" -gt "$MAX_CONTEXT" ]; then
  CONTEXT=$(printf '%s' "$CONTEXT" | cut -c1-"$MAX_CONTEXT")
  CONTEXT="${CONTEXT}…"
fi

ESCAPED=$(json_escape "$CONTEXT")

case "$HOST" in
  claude-code)
    printf '%s\n' "{\"hookSpecificOutput\":{\"hookEventName\":\"SessionStart\",\"additionalContext\":\"${ESCAPED}\"}}"
    ;;
  cursor)
    printf '%s\n' "{\"additional_context\":\"${ESCAPED}\"}"
    ;;
  *)
    printf '%s\n' "{\"additional_context\":\"${ESCAPED}\"}"
    ;;
esac

exit 0
