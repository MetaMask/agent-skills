# Capabilities and consent

Declare what each command needs on `package.json` at `mm.commands` `capabilities`.
Users approve at install.
They approve again on `plugins update` if the manifest hash or version changed.

## Active capabilities

`wallet-read` grants read services and authenticated RPC.
Typical APIs are `walletStateManager`, `accountService`, `priceService`, `tokenService`,
`feesService`, `swapQuoteStore`, `authService`, and `publicClient`.

`wallet-submit` grants sign and submit through `ctx.walletExecutor`.
MetaMask policy still applies.

`network-manage` grants `networkRegistry`.

If a command uses a gated API without the capability, the host throws
`PERMISSION_DENIED`.

The consent screen treats `wallet-submit` and `network-manage` as sensitive.

## Reserved capabilities

Do not declare `mnemonic-read`.
The secret recovery phrase and `mnemonicStore` are host-only.

Do not declare `config-write`.
It is not implemented.

Manifest parse rejects both.

## dataAccess

These labels feed the consent UI.
They are not extra runtime keys.
Use the smallest honest set from `accounts`, `balances`, `prices`, `tokens`, `network`,
`fees`, `swap-quotes`, `session`, and `mnemonic`.

Declaring `mnemonic` in `dataAccess` does not grant secret recovery phrase access.

## Runtime grant

Approvals live in `~/.metamask/config.json`.
The effective grant is the intersection of declared command capabilities and
`approvedCapabilities`.
A version or `manifestHash` mismatch yields empty grants until the user reinstalls or
updates and consents again.

## Host-only accessors

`ctx.session` and the CLI token always throw `PERMISSION_DENIED`.

`ctx.mnemonicStore` and the secret recovery phrase always throw `PERMISSION_DENIED`.

Use `walletStateManager` and `walletExecutor` instead.

## Plugin-wide list

Keep plugin-level `mm.capabilities` as an empty array.
Plugin-level capabilities are merged into every command.
