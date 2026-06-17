#!/usr/bin/env python3
"""Pay an HTTP 402 (x402) request with the active wallet.

Fetches a paywalled URL, reads the server's x402 payment requirements, signs an
EIP-3009 authorization with `mm wallet sign-typed-data`, retries with the
payment header, and reports the settlement. Supports x402 protocol v1
(X-PAYMENT) and v2 (PAYMENT-SIGNATURE). Signing is delegated to `mm`, so the
private key stays in the wallet.

Usage:
    python3 x402_pay.py inspect <url> [--method M] [--data BODY]
    python3 x402_pay.py pay <url> --confirm [--method M] [--data BODY]
                                  [--asset <contract>] [--network <network>]

`inspect` fetches the URL and prints the payment requirement(s) as JSON
(asset, amount, network, payTo, resource) without signing or spending. Review
this before paying.

`pay` runs the payment for a single offered option and prints the settlement
(transaction hash) and the resource body. It requires --confirm. When the 402
offers more than one eligible option, select one with --asset or --network.

The resource may use any HTTP method; pass --method (and --data for a request
body) and the same request is replayed with the payment attached.

The script pays the exact scheme on networks `mm` supports; which currencies
and amounts are allowed is the wallet's decision at signing. Each run makes one
payment with a single retry; rerunning makes a new payment, so guard repeated
calls at the caller. A local idempotency ledger is a possible future addition.

Examples:
    python3 x402_pay.py inspect https://api.example.com/premium
    python3 x402_pay.py pay https://api.example.com/premium --confirm
"""

import argparse
import base64
import json
import re
import secrets
import subprocess
import sys
import time
import urllib.error
import urllib.request
from decimal import Decimal
from urllib.parse import urlparse

ADDRESS_RE = re.compile(r"^0x[0-9a-fA-F]{40}$")
LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}


class CeremonyError(Exception):
    """An expected failure to surface to the caller."""


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Surfaces redirects instead of following them.

    A cross-host redirect on a payment request could divert payment to a host
    the user never chose, so the 3xx is returned and rejected by the caller.
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_OPENER = urllib.request.build_opener(_NoRedirect)


def _check_url(url):
    """Reject plaintext URLs so a payment is never sent over http.

    Loopback is exempt to allow testing against a local resource server.
    """
    parsed = urlparse(url)
    if parsed.scheme == "https":
        return
    if parsed.scheme == "http" and parsed.hostname in LOOPBACK_HOSTS:
        return
    raise CeremonyError("resource URL must be https:// (http allowed only on loopback)")


def http(url, method="GET", headers=None, body=None):
    """Make a request. Returns (status, headers, body_bytes); no raise on 4xx/5xx."""
    _check_url(url)
    req = urllib.request.Request(url, data=body, method=method, headers=headers or {})
    try:
        resp = _OPENER.open(req, timeout=30)
        return resp.status, resp.headers, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read()


def request_parts(data, content_type):
    """Turn an optional request body string into (bytes, headers) for replay.

    x402 is method-agnostic, so a paid POST must be sent identically on both the
    initial request and the retry that carries the payment.
    """
    if data is None:
        return None, {}
    return data.encode("utf-8"), {"Content-Type": content_type}


def _mm_json(args):
    """Run an `mm` command and return its JSON result.

    The JSON is sliced out of stdout because `mm` may emit non-JSON warnings
    (e.g. Node startup notices) around it.
    """
    out = subprocess.run(["mm", *args], capture_output=True, text=True)
    text = out.stdout
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise CeremonyError("mm produced no JSON (%s): %s" % (out.returncode, out.stderr.strip()))
    return json.loads(text[start:end + 1])


_chains_cache = None


def _chains():
    """Return mm's supported chains, so network support stays the wallet's call."""
    global _chains_cache
    if _chains_cache is None:
        _chains_cache = (_mm_json(["chains", "list", "--json"]).get("data") or {}).get("chains", [])
    return _chains_cache


def chain_id_for(network):
    """Resolve an x402 network identifier to an EVM chain id.

    Accepts v2 CAIP-2 ids (e.g. "eip155:8453") directly and v1 network names
    (e.g. "base-sepolia") by matching mm's chain list.
    """
    if network.startswith("eip155:"):
        try:
            return int(network.split(":", 1)[1])
        except ValueError:
            raise CeremonyError("unparseable CAIP-2 network: %s" % network)
    for c in _chains():
        if network in (c.get("key"), c.get("caip2")) or network.lower() == (c.get("name") or "").lower():
            return c.get("chainId")
    raise CeremonyError("network '%s' is not supported by mm (see `mm chains list`)" % network)


_asset_meta_cache = {}


def asset_meta(chain_id, asset):
    """Look up an asset's symbol and decimals from mm, for display only.

    Returns None when mm cannot resolve it (e.g. testnets the Token API does
    not index); the signed amount is the server's atomic value regardless.
    """
    if chain_id is None or not asset:
        return None
    key = (chain_id, asset.lower())
    if key not in _asset_meta_cache:
        meta = None
        try:
            res = _mm_json(["token", "assets", "--asset-ids",
                            "eip155:%s/erc20:%s" % (chain_id, asset), "--json"])
            assets = (res.get("data") or {}).get("assets") or []
            if assets and assets[0].get("decimals") is not None:
                meta = {"symbol": assets[0].get("symbol"), "decimals": assets[0]["decimals"]}
        except (CeremonyError, ValueError):
            meta = None
        _asset_meta_cache[key] = meta
    return _asset_meta_cache[key]


def parse_402(status, headers, body):
    """Return (version, [normalized_option, ...]). Raises if not a usable 402."""
    if status != 402:
        raise CeremonyError("expected HTTP 402, got %s" % status)

    # v2 carries requirements in the PAYMENT-REQUIRED header; v1 in the body.
    # The accepts[] array is what marks a response as a standard x402 challenge:
    # other paywalls also answer 402 but with their own, unsupported schemes.
    pr = headers.get("PAYMENT-REQUIRED")
    if pr:
        try:
            data = json.loads(base64.b64decode(pr))
        except (ValueError, UnicodeDecodeError) as e:
            raise CeremonyError("could not parse the PAYMENT-REQUIRED header: %s" % e)
        version = 2
    else:
        try:
            data = json.loads(body.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as e:
            raise CeremonyError("could not parse the 402 response body: %s" % e)
        version = 1
        # No PAYMENT-REQUIRED header and no accepts[] means another paywall
        # scheme answering 402, not x402.
        if not isinstance(data, dict) or "accepts" not in data:
            raise CeremonyError(
                "received HTTP 402 but it is not a standard x402 challenge "
                "(no PAYMENT-REQUIRED header and no accepts[] in the body); "
                "this endpoint uses a payment scheme this script does not support")

    accepts = (data.get("accepts") if isinstance(data, dict) else None) or []

    options = []
    for a in accepts:
        amount = a.get("amount", a.get("maxAmountRequired"))
        options.append({
            "scheme": a.get("scheme"),
            "network": a.get("network"),
            "amount": str(amount) if amount is not None else None,
            "payTo": a.get("payTo"),
            "asset": a.get("asset"),
            "maxTimeoutSeconds": a.get("maxTimeoutSeconds", 60),
            "extra": a.get("extra", {}),
            "resource": a.get("resource"),
        })
    if not options:
        raise CeremonyError("402 had no payment options")
    return version, options


def describe(option):
    """Annotate an option with chain and display metadata; never raises."""
    out = dict(option)
    try:
        chain_id = chain_id_for(option["network"])
    except CeremonyError:
        chain_id = None
    out["chainId"] = chain_id
    out["eligible"] = chain_id is not None and option.get("scheme") == "exact"
    meta = asset_meta(chain_id, option.get("asset"))
    if meta:
        out["symbol"] = meta["symbol"]
        out["decimals"] = meta["decimals"]
        amount = option.get("amount")
        if isinstance(amount, str) and amount.isdigit():
            out["humanAmount"] = str(Decimal(amount) / (Decimal(10) ** meta["decimals"]))
    return out


def select(options, want_asset=None, want_network=None):
    """Pick the single payable option, or raise so the caller can react.

    Requires exactly one option with the exact scheme on a network mm supports;
    --asset/--network narrow the choice when a server offers several, since
    picking one silently could spend on an asset the user did not intend.
    """
    described = [describe(o) for o in options]
    eligible = []
    for d in described:
        if not d["eligible"]:
            continue
        if want_asset and (d.get("asset") or "").lower() != want_asset.lower():
            continue
        if want_network and d.get("network") != want_network:
            continue
        eligible.append(d)
    if not eligible:
        raise CeremonyError(
            "no eligible option (need scheme 'exact' on a network mm supports). "
            "Offered: %s" % json.dumps(described))
    if len(eligible) > 1:
        raise CeremonyError(
            "multiple eligible options; disambiguate with --asset/--network. "
            "Eligible: %s" % json.dumps(eligible))
    return eligible[0]


def wallet_address():
    """Return the active wallet address, the payer for the authorization."""
    d = _mm_json(["wallet", "address", "--json"]).get("data")
    return d["address"] if isinstance(d, dict) else d


def sign_typed_data(chain_id, payload, intent):
    """Sign EIP-712 typed data with `mm`, keeping the key inside the wallet."""
    res = _mm_json(["wallet", "sign-typed-data", "--chain-id", str(chain_id),
                    "--wait", "--json", "--intent", intent,
                    "--payload", json.dumps(payload)])
    sig = (res.get("data") or {}).get("signature")
    if not res.get("ok") or not sig:
        raise CeremonyError("signing failed: %s" % json.dumps(res))
    return sig


def build_typed_data(option, chain_id, from_addr):
    """Build the EIP-3009 TransferWithAuthorization message to sign.

    validBefore honors the server's maxTimeoutSeconds so the facilitator can
    settle within the window it asked for; any ceiling on how long an
    authorization may live is the wallet's policy, not a constant here. A random
    nonce keeps each authorization single-use.
    """
    nonce = "0x" + secrets.token_bytes(32).hex()
    valid_before = str(int(time.time()) + int(option["maxTimeoutSeconds"]))
    authorization = {
        "from": from_addr,
        "to": option["payTo"],
        "value": option["amount"],
        "validAfter": "0",
        "validBefore": valid_before,
        "nonce": nonce,
    }
    typed_data = {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "TransferWithAuthorization": [
                {"name": "from", "type": "address"},
                {"name": "to", "type": "address"},
                {"name": "value", "type": "uint256"},
                {"name": "validAfter", "type": "uint256"},
                {"name": "validBefore", "type": "uint256"},
                {"name": "nonce", "type": "bytes32"},
            ],
        },
        "primaryType": "TransferWithAuthorization",
        "domain": {
            "name": option["extra"].get("name"),
            "version": option["extra"].get("version"),
            "chainId": chain_id,
            "verifyingContract": option["asset"],
        },
        "message": authorization,
    }
    return typed_data, authorization


def validate(option, chain_id):
    """Check the offer is structurally sound before signing.

    Currency and spend policy are the wallet's responsibility; this only
    guards protocol correctness so a malformed offer is never signed.
    """
    if option["scheme"] != "exact":
        raise CeremonyError("scheme must be 'exact', got %r" % option["scheme"])
    if chain_id is None:
        raise CeremonyError("network %r is not supported by mm" % option.get("network"))
    if not option["asset"] or not ADDRESS_RE.match(option["asset"]):
        raise CeremonyError("asset is not a valid contract address: %r" % option.get("asset"))
    if not option["amount"] or not option["amount"].isdigit() or int(option["amount"]) <= 0:
        raise CeremonyError("amount must be a positive atomic-unit integer, got %r" % option["amount"])
    if not option["payTo"] or not ADDRESS_RE.match(option["payTo"]):
        raise CeremonyError("payTo is not a valid address: %r" % option["payTo"])
    if not option["extra"].get("name") or not option["extra"].get("version"):
        raise CeremonyError("402 option missing EIP-712 domain name/version in 'extra'")


def settlement(headers, version):
    """Decode the facilitator's settlement receipt, if the server sent one."""
    name = "X-PAYMENT-RESPONSE" if version == 1 else "PAYMENT-RESPONSE"
    raw = headers.get(name)
    if not raw:
        return None
    return json.loads(base64.b64decode(raw))


def cmd_inspect(url, method, data, content_type):
    """Print the 402 payment requirement(s) without signing or spending."""
    body, headers = request_parts(data, content_type)
    status, rheaders, rbody = http(url, method, headers, body)
    version, options = parse_402(status, rheaders, rbody)
    print(json.dumps({
        "status": "payment_required",
        "x402Version": version,
        "options": [describe(o) for o in options],
    }, indent=2))


def cmd_pay(url, method, data, content_type, confirm, want_asset, want_network):
    """Run the payment for one offered option and print the settlement."""
    if not confirm:
        raise CeremonyError("refusing to pay without --confirm; run 'inspect' first and "
                            "get user approval, then re-run 'pay <url> --confirm'")
    body, headers = request_parts(data, content_type)
    # Fetch fresh so the short 402 window is never stale.
    status, rheaders, rbody = http(url, method, headers, body)
    version, options = parse_402(status, rheaders, rbody)
    option = select(options, want_asset, want_network)
    chain_id = option["chainId"]
    validate(option, chain_id)

    from_addr = wallet_address()
    typed_data, authorization = build_typed_data(option, chain_id, from_addr)

    intent = "x402: %s %s to %s for %s" % (
        option.get("humanAmount", option["amount"]), option.get("symbol", ""),
        option["payTo"], url)
    signature = sign_typed_data(chain_id, typed_data, intent)

    payment = {"x402Version": version, "scheme": option["scheme"],
               "network": option["network"],
               "payload": {"signature": signature, "authorization": authorization}}
    b64 = base64.b64encode(json.dumps(payment).encode()).decode()
    header = "X-PAYMENT" if version == 1 else "PAYMENT-SIGNATURE"

    # Replay the same request with the payment attached.
    status, rheaders, rbody = http(url, method, dict(headers, **{header: b64}), body)
    if status != 200:
        # One attempt only: do not retry a payment.
        raise CeremonyError("payment not accepted (HTTP %s): %s" % (status, rbody.decode("utf-8", "replace")))

    settle = settlement(rheaders, version)
    try:
        resource = json.loads(rbody.decode("utf-8"))
    except ValueError:
        resource = rbody.decode("utf-8", "replace")
    print(json.dumps({
        "status": "settled",
        "asset": option.get("symbol", option["asset"]),
        "amount": option.get("humanAmount", option["amount"]),
        "network": option["network"],
        "payTo": option["payTo"],
        "transaction": (settle or {}).get("transaction") or (settle or {}).get("txHash"),
        "settlement": settle,
        "resource": resource,
    }, indent=2))


def main(argv=None):
    """Parse arguments and report CeremonyError as JSON on stderr."""
    parser = argparse.ArgumentParser(description="Pay an HTTP 402 (x402) request with the active wallet.")
    sub = parser.add_subparsers(dest="command", required=True)

    for p in (sub.add_parser("inspect", help="Fetch and parse a 402 (read-only)."),
              sub.add_parser("pay", help="Run the full payment ceremony.")):
        p.add_argument("url")
        p.add_argument("--method", default="GET",
                       help="HTTP method to request the resource with (default GET).")
        p.add_argument("--data", help="Request body to send (and replay on the paid retry).")
        p.add_argument("--content-type", default="application/json",
                       help="Content-Type for --data (default application/json).")

    p_pay = sub.choices["pay"]
    p_pay.add_argument("--confirm", action="store_true",
                       help="Required. Explicit user approval to sign and spend.")
    p_pay.add_argument("--asset", help="Disambiguate by asset contract when multiple are offered.")
    p_pay.add_argument("--network", help="Disambiguate by network when multiple are offered.")

    args = parser.parse_args(argv)
    try:
        if args.command == "inspect":
            cmd_inspect(args.url, args.method.upper(), args.data, args.content_type)
        else:
            cmd_pay(args.url, args.method.upper(), args.data, args.content_type,
                    args.confirm, args.asset, args.network)
    except CeremonyError as e:
        print(json.dumps({"status": "error", "error": str(e)}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
