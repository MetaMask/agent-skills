# Verify a wallet action before signing (optional / secondary)

> **Secondary to the trade-reasoning check.** This authorization axis overlaps with what
> MetaMask's `wallet policy` (outflow caps, whitelists) and `guard` trading-mode already do
> deterministically — much of it *is* reducible to rules. It's documented here because it was
> built and dryrun-verified, not because it's the reason to install this skill. The core value
> is [verify-trade.md](verify-trade.md), the reasoning check that a rule can't replace.

Use before any state-changing wallet command (`approve`, `transfer`, `permit`, `bridge`,
`swap`) when an agent proposes it autonomously. Checks whether the action is authorized by
and minimally scoped to the user's mandate — catches honest-but-over-scoped actions that
pass Blockaid and policy and still drain the wallet.

## When to run

After the agent proposes a wallet action, before the mapped `mm` command runs.

## Call

```
verdict = thoughtproof.verify({
  mode: "action_authorization",
  claim: "<the proposed action: approve/transfer/permit/bridge/swap + params>",
  evidence: "<the user's mandate + concrete args (spender, recipient, amount, chain)>",
  mandate: { ... },   // optional machine-readable mandate; activates the deterministic gate
})
```

The four `action_authorization` gold steps — scope containment, recipient integrity,
mandate alignment, least-privilege — run on the live Sentinel API and BLOCK the categorical
drain vectors.

## Gate → mm command mapping (v4.0.0)

Only on `ALLOW`, map the action to the `mm` command (args passed as a vector to `execFile`
— no shell, no injection):

| Action | `mm` command (v4.0.0) |
|---|---|
| `approve` | `mm wallet send-transaction --chain-id <id> --payload '<JSON>'` (ERC-20 approval = raw call; no high-level approve in v4.0.0) |
| `transfer` | `mm transfer --to <address> --amount <value> --chain-id <id> --token <symbol-or-address> --json` |
| `swap` | `mm swap execute --from <token> --to <token> --amount <amount> --from-chain <id> [--slippage <percent>] --json` |
| `bridge` | `mm swap execute --from <token> --to <token> --amount <amount> --from-chain <id> --to-chain <dest> --json` (cross-chain swap; no `mm bridge` in v4.0.0) |
| `permit` | `mm wallet sign-typed-data --chain-id <id> --payload '<JSON>'` (EIP-712 permit doc) |

On `UNCERTAIN` or `BLOCK`: `mm` is never invoked; surface the objections.

## Honesty

- Verdicts are real `action_authorization` calls. The deterministic gate (mandate +
  gateMode) activates automatically server-side; until then it degrades to the LLM path.
- Command names verified against `@metamask/agentic-cli` v4.0.0 (flags checked via
  `mm <cmd> --help`, 2026-07-07). Re-check if your installed `mm` differs.
- **Verifies authorization scope, does not guarantee safety.** An ALLOW means the action is
  in-scope and minimally scoped to the stated mandate — not that it is risk-free.
- Additive to MetaMask's guard mode + Blockaid, not a replacement.
