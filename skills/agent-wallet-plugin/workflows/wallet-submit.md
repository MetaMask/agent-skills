# Add a wallet-submit command

Use this how-to when the command signs a message or typed data, or sends a transaction.

## Confirm with the user

Before you implement or run a live submit, confirm chain, `to`, value, and the intent
summary.
Do not send real funds in examples without explicit approval.

## Manifest

```json
{
  "id": "pons:buy",
  "capabilities": ["wallet-submit"],
  "dataAccess": ["accounts"]
}
```

If the command also reads chain state first, add `wallet-read` on that command only.

## Quote then submit

Prefer a `--confirm` boolean that defaults to false.
Compute the plan without `walletExecutor`, print it, and submit only when `--confirm`
is set.
Headless agents must pass `--confirm` after the user agrees.

## Executor

```ts
const executor = await this.ctx.walletExecutor(io, this.pluginCommandId, {
  emitStepNotices: true,
});
type WalletRequest = Parameters<typeof executor>[0];
```

Use `emitStepNotices` for multi-step flows such as approve then trade.

Cast structurally with `as unknown as WalletRequest`.
Check result `kind` and `hash` or `signature`.

Jobs may poll and emit `AWAITING_MFA`.
Treat that as waiting, not failure.
The user can run `mm wallet requests watch` with the polling id.

## Policy

`wallet-submit` is still gated by MetaMask wallet policy, including guard, beast, and
MFA.
Do not tell the user the plugin bypasses policy.

## Test

Auth and init are required.
Rebuild and reinstall.
A capability change needs fresh consent.
Use a test chain or a dry-run path first.
