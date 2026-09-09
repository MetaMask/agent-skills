# Plugin context

During `execute`, `this.ctx` is a `PluginCommandContext`.
`logger`, `args`, `flags`, and `argv` are always available.
Everything else is capability-gated.

## Read path with wallet-read

```ts
const state = this.ctx.walletStateManager.read();
const address =
  state.selectedWallet?.namespace === "evm"
    ? /* resolve from selected + byokWallets / remoteWallets */
    : ([...state.byokWallets, ...state.remoteWallets][0]?.address ?? "");

const client = this.ctx.publicClient(1);
const balanceWei = await client.getBalance({
  address: address as `0x${string}`,
});
```

`publicClient` takes a numeric chain id and returns an authenticated viem
`PublicClient` on the same Infura gateway the host uses.
The client may have no chain definition attached.
Pass explicit contract addresses for ENS and similar actions.

Prefer the selected EVM wallet when `state.selectedWallet` is an EVM wallet.
Filter `byokWallets` and `remoteWallets` by `namespace === "evm"` and match
`state.selectedWallet`.
The `mm-plugin-pons` helper `resolveEvmAddress` shows this pattern.

## Submit path with wallet-submit

```ts
const executor = await this.ctx.walletExecutor(io, this.pluginCommandId);
```

Pass `{ emitStepNotices: true }` as the third argument for multi-step flows such as
approve then trade.

`EvmWalletRequest` is not exported.
Shape the request structurally and cast it.

### Transaction request

```ts
type WalletRequest = Parameters<typeof executor>[0];
const result = await executor({
  kind: "transaction",
  chainId,
  transaction: { to, data, value },
  intent: { summary, action: "call", details: { ... } },
} as unknown as WalletRequest);
```

Expect `result.kind === "transaction"` and `result.hash`.

### Typed data request

```ts
const result = await executor({
  kind: "typed-data",
  chainId,
  typedData,
} as unknown as WalletRequest);
```

Expect `result.kind === "signature"` and `result.signature`.

Pass `this.pluginCommandId` as the source string, which is the second argument.
The host audits that id.

## Not on the context

`session`, `mnemonicStore`, and `createAppContext` are not available.
Do not import host internals to reach them.
