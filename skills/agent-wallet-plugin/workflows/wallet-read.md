# Add a wallet-read command

Use this how-to when the command needs balances, prices, tokens, a wallet list, or raw
EVM RPC.

## Manifest

```json
{
  "id": "demo:balance",
  "capabilities": ["wallet-read"],
  "dataAccess": ["balances", "accounts"]
}
```

Keep plugin-wide `capabilities` empty.

## Command

Leave `static override requiresAuth = true`, which is the default.

Leave `requiresInit` true unless the command only needs auth without a configured
wallet. That case is rare.

```ts
const state = this.ctx.walletStateManager.read();
const client = this.ctx.publicClient(chainId);
```

Resolve the selected EVM address when `state.selectedWallet` is EVM.
Otherwise use the first EVM BYOK wallet, then the first remote wallet.
If there is no wallet, throw `CommandError` with a hint to run `mm init`.

## RPC

`publicClient` has no mnemonic.
Use `readContract`, `getBalance`, and ENS helpers.
Pass explicit resolver addresses when the client has no chain object, such as ENS on
mainnet.

## Test

The user must be logged in with `mm login` and is typically initialized with `mm init`.
Confirm before any network-heavy loops.
Rebuild, reinstall, and run with `--json`.
