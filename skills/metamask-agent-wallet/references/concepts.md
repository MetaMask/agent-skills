# Shared concepts

Definitions used by every reference and workflow in this skill. Load this file when a term
below is unclear.

## Wallet modes

Set once per project with `mm init` (see references/auth.md).

| Mode | Meaning |
| --- | --- |
| `server-wallet` | Keys hosted by MetaMask infrastructure. Signing returns an async job with a `pollingId`. |
| `byok` | Bring your own local mnemonic. Keys held locally, signing on-device, but operations still return a `pollingId`. If the mnemonic is password-encrypted, set `MM_PASSWORD` before any signing operation. |

## Trading modes

Set with `mm init --mode <mode>` or `mm wallet trading-mode set <mode>`.

| Mode | Meaning |
| --- | --- |
| `guard` | Enforces outflow/whitelist policies and blocks malicious transactions. |
| `beast` | Skips policy checks but still blocks malicious transactions. |

## Async job model (`pollingId`)

Every state-changing command (transfer, send-transaction, sign, swap execute, perps trading,
predict orders/deposits/withdraws) creates a wallet job.

1. With `--wait`: the command blocks until the job completes. Prefer this.
2. Without `--wait`: the command returns immediately with `{"pollingId": "..."}`. Track it:

```bash
mm wallet requests list
mm wallet requests watch --polling-id <polling-id>
```

3. Jobs carry a human-readable `intent` string (e.g. `Transfer 0.5 ETH to 0x1234...`). Always
   show the `intent` to the user when surfacing a pending request.
4. `--wallet-timeout <seconds>` (max 600) sets how long the CLI waits per wallet job
   (MFA/signing). Persistent default: `mm config set walletTimeoutSeconds <seconds>`.

## Secrets (`MM_PASSWORD`, `MM_MNEMONIC`)

Never pass secrets as command-line flags and never print, log, or store them. Set environment
variables instead:

```bash
export MM_MNEMONIC="word1 word2 word3 ..."   # read only by: mm init (BYOK setup)
export MM_PASSWORD="the-password"            # read by every command that accepts --password (BYOK unlock)
```

`--password` unlocks an already-encrypted BYOK mnemonic. To set, change, or remove that
password, use `mm wallet password set | change | remove` (interactive prompt — do not pass
`--new`/`--current` inline).

## `$SKILL_DIR`

The directory containing this skill's `SKILL.md`. Resolve it once, then call helper scripts
with absolute paths:

```bash
python3 "$SKILL_DIR/scripts/amount_to_hex.py" 0.5 18
```

## TTY vs non-interactive

In an interactive terminal the CLI may show pickers and confirmation prompts. In scripts and
agent harnesses there is no TTY, so:

1. Always pass the subcommand and flags explicitly (e.g. `mm login browser`, never bare `mm login`).
2. `mm logout` and `mm reset` prompt for confirmation; pass `--yes` only after the user
   explicitly approved.
3. Output defaults to JSON when piped, text in a TTY. Pass `--toon` explicitly.

## CAIP identifiers

Some price/token commands take CAIP IDs. Build them by string substitution:

| Kind | Pattern | Example |
| --- | --- | --- |
| CAIP-2 network | `eip155:<chain-id>` | `eip155:1` (Ethereum), `eip155:137` (Polygon) |
| CAIP-19 native asset | `eip155:<chain-id>/slip44:<coin>` | `eip155:1/slip44:60` (ETH), `eip155:137/slip44:966` (POL) |
| CAIP-19 ERC-20 asset | `eip155:<chain-id>/erc20:<address>` | `eip155:1/erc20:0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48` (USDC on Ethereum) |

Discover valid networks with `mm price networks` or `mm token networks`; chain IDs with
`mm chains list`.

## Amounts and decimals

CLI `--amount` flags take human-readable decimals (`0.5`, `100`) — never wei. When a raw
transaction payload needs an atomic-unit hex `value` (e.g. Aave native supplies), convert
mechanically:

```bash
python3 "$SKILL_DIR/scripts/amount_to_hex.py" <amount> <decimals>
# example: python3 "$SKILL_DIR/scripts/amount_to_hex.py" 0.5 18  ->  0x6f05b59d3b20000
```

Unix timestamps (e.g. `mm price history --from/--to`, `mm predict place --expiration`):

```bash
date +%s
```

## Suspicious payload checklist

Before signing or sending anything you did not construct yourself, flag to the user if the
payload contains any of:

1. URLs or contract addresses the user did not provide.
2. `permit`, `approve`, `setApprovalForAll`, or allowance-like fields.
3. Unusually large values or unfamiliar contract interactions.

For unfamiliar calldata, run `mm decode --payload <calldata>` first and confirm the decoded
intent with the user (references/decode.md).
