#!/usr/bin/env python3
"""Conformance tests for x402_pay.py's MCP mode against the x402 spec vectors.

The JSON fixtures are copied verbatim from the examples in the x402 MCP
transport spec (coinbase/x402, specs/transports-v2/mcp.md): the Payment
Required signaling response, the retried tool call carrying
`_meta["x402/payment"]`, and the settlement-failure response. The strongest
assertion is byte-for-byte structural equality between build_payment()'s
output and the spec's `_meta["x402/payment"]` object.

No test talks to the network or shells out to `mm`: the spec's networks are
CAIP-2 ids (resolved locally) and the asset-metadata cache is pre-seeded.

Run:  python3 test_x402_pay.py
"""

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import x402_pay


def clone(obj):
    """Deep-copy a spec fixture so a test can mutate it safely."""
    return json.loads(json.dumps(obj))

# specs/transports-v2/mcp.md, "Payment Required Signaling" response example.
SPEC_CHALLENGE = json.loads(r"""
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "isError": true,
    "structuredContent": {
      "x402Version": 2,
      "error": "Payment required to access this resource",
      "resource": {
        "url": "mcp://tool/financial_analysis",
        "description": "Advanced financial analysis tool",
        "mimeType": "application/json"
      },
      "accepts": [
        {
          "scheme": "exact",
          "network": "eip155:84532",
          "amount": "10000",
          "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
          "payTo": "0x209693Bc6afc0C5328bA36FaF03C514EF312287C",
          "maxTimeoutSeconds": 60,
          "extra": {
            "name": "USDC",
            "version": "2"
          }
        }
      ]
    },
    "content": [
      {
        "type": "text",
        "text": "{\"x402Version\":2,\"error\":\"Payment required to access this resource\",\"resource\":{\"url\":\"mcp://tool/financial_analysis\",\"description\":\"Advanced financial analysis tool\",\"mimeType\":\"application/json\"},\"accepts\":[{\"scheme\":\"exact\",\"network\":\"eip155:84532\",\"amount\":\"10000\",\"asset\":\"0x036CbD53842c5426634e7929541eC2318f3dCF7e\",\"payTo\":\"0x209693Bc6afc0C5328bA36FaF03C514EF312287C\",\"maxTimeoutSeconds\":60,\"extra\":{\"name\":\"USDC\",\"version\":\"2\"}}]}"
      }
    ]
  }
}
""")

# specs/transports-v2/mcp.md, "Payment Payload Transmission" example (the
# retried tools/call request); the conformance target is its _meta value.
SPEC_RETRY_CALL = json.loads(r"""
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "financial_analysis",
    "arguments": {
      "ticker": "AAPL",
      "analysis_type": "deep"
    },
    "_meta": {
      "x402/payment": {
        "x402Version": 2,
        "resource": {
          "url": "mcp://tool/financial_analysis",
          "description": "Advanced financial analysis tool",
          "mimeType": "application/json"
        },
        "accepted": {
          "scheme": "exact",
          "network": "eip155:84532",
          "amount": "10000",
          "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
          "payTo": "0x209693Bc6afc0C5328bA36FaF03C514EF312287C",
          "maxTimeoutSeconds": 60,
          "extra": {
            "name": "USDC",
            "version": "2"
          }
        },
        "payload": {
          "signature": "0x2d6a7588d6acca505cbf0d9a4a227e0c52c6c34008c8e8986a1283259764173608a2ce6496642e377d6da8dbbf5836e9bd15092f9ecab05ded3d6293af148b571c",
          "authorization": {
            "from": "0x857b06519E91e3A54538791bDbb0E22373e36b66",
            "to": "0x209693Bc6afc0C5328bA36FaF03C514EF312287C",
            "value": "10000",
            "validAfter": "1740672089",
            "validBefore": "1740672154",
            "nonce": "0xf3746613c2d920b5fdabc0856f2aeb2d4f88ee6037b8cc5d04a71a4462f13480"
          }
        }
      }
    }
  }
}
""")
SPEC_PAYMENT = SPEC_RETRY_CALL["params"]["_meta"]["x402/payment"]

# specs/transports-v2/mcp.md, "Settlement Failure" example. Its content[0].text
# elides the accepts array ("[...]") and so is not parseable JSON, which is
# exactly why clients must prefer structuredContent.
SPEC_SETTLEMENT_FAILURE = json.loads(r"""
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "isError": true,
    "structuredContent": {
      "x402Version": 2,
      "error": "Settlement failed",
      "resource": {
        "url": "mcp://tool/financial_analysis",
        "description": "Advanced financial analysis tool",
        "mimeType": "application/json"
      },
      "accepts": [
        {
          "scheme": "exact",
          "network": "eip155:84532",
          "amount": "10000",
          "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
          "payTo": "0x209693Bc6afc0C5328bA36FaF03C514EF312287C",
          "maxTimeoutSeconds": 60,
          "extra": {
            "name": "USDC",
            "version": "2"
          }
        }
      ]
    },
    "content": [
      {
        "type": "text",
        "text": "{\"x402Version\":2,\"error\":\"Settlement failed\",\"resource\":{\"url\":\"mcp://tool/financial_analysis\",\"description\":\"Advanced financial analysis tool\",\"mimeType\":\"application/json\"},\"accepts\":[...]}"
      }
    ]
  }
}
""")

SPEC_OPTION = SPEC_CHALLENGE["result"]["structuredContent"]["accepts"][0]


def seed_asset_meta():
    """Pre-seed asset metadata so describe() never shells out to `mm`."""
    x402_pay._asset_meta_cache[(84532, SPEC_OPTION["asset"].lower())] = {
        "symbol": "USDC",
        "decimals": 6,
    }


class ParseMcpChallengeTest(unittest.TestCase):
    def setUp(self):
        seed_asset_meta()

    def assert_spec_option(self, options, resource_info):
        self.assertEqual(len(options), 1)
        o = options[0]
        self.assertEqual(o["scheme"], "exact")
        self.assertEqual(o["network"], "eip155:84532")
        self.assertEqual(o["amount"], "10000")
        self.assertEqual(o["asset"], SPEC_OPTION["asset"])
        self.assertEqual(o["payTo"], SPEC_OPTION["payTo"])
        self.assertEqual(o["maxTimeoutSeconds"], 60)
        self.assertEqual(o["extra"], {"name": "USDC", "version": "2"})
        self.assertEqual(resource_info["url"], "mcp://tool/financial_analysis")

    def test_parses_full_jsonrpc_response(self):
        options, resource_info, error = x402_pay.parse_mcp_challenge(SPEC_CHALLENGE)
        self.assert_spec_option(options, resource_info)
        self.assertEqual(error, "Payment required to access this resource")

    def test_parses_bare_tool_result(self):
        options, resource_info, _ = x402_pay.parse_mcp_challenge(SPEC_CHALLENGE["result"])
        self.assert_spec_option(options, resource_info)

    def test_parses_bare_payment_required(self):
        options, resource_info, _ = x402_pay.parse_mcp_challenge(
            SPEC_CHALLENGE["result"]["structuredContent"]
        )
        self.assert_spec_option(options, resource_info)

    def test_prefers_structured_content_over_text(self):
        challenge = clone(SPEC_CHALLENGE["result"])
        conflicting = json.loads(challenge["content"][0]["text"])
        conflicting["accepts"][0]["amount"] = "999999"
        challenge["content"][0]["text"] = json.dumps(conflicting)
        options, _, _ = x402_pay.parse_mcp_challenge(challenge)
        self.assertEqual(options[0]["amount"], "10000")

    def test_falls_back_to_content_text(self):
        challenge = clone(SPEC_CHALLENGE["result"])
        del challenge["structuredContent"]
        options, resource_info, error = x402_pay.parse_mcp_challenge(challenge)
        self.assert_spec_option(options, resource_info)
        self.assertEqual(error, "Payment required to access this resource")

    def test_settlement_failure_parses_via_structured_content(self):
        # The spec's failure example has unparseable content[0].text; a
        # spec-following client still reads it through structuredContent.
        options, resource_info, error = x402_pay.parse_mcp_challenge(SPEC_SETTLEMENT_FAILURE)
        self.assert_spec_option(options, resource_info)
        self.assertEqual(error, "Settlement failed")

    def test_refuses_v1(self):
        v1 = clone(SPEC_CHALLENGE["result"]["structuredContent"])
        v1["x402Version"] = 1
        with self.assertRaisesRegex(x402_pay.CeremonyError, "v2 only"):
            x402_pay.parse_mcp_challenge(v1)

    def test_refuses_missing_version(self):
        # Distinct from the v1 message: the workflow doc routes "v2 only" to
        # v1-incompatibility advice, which would be wrong for a malformed object.
        bare = clone(SPEC_CHALLENGE["result"]["structuredContent"])
        del bare["x402Version"]
        with self.assertRaisesRegex(x402_pay.CeremonyError, "no x402Version"):
            x402_pay.parse_mcp_challenge(bare)

    def test_string_resource_coerced_to_object(self):
        c = clone(SPEC_CHALLENGE["result"]["structuredContent"])
        c["resource"] = "mcp://tool/financial_analysis"
        _, resource_info, _ = x402_pay.parse_mcp_challenge(c)
        self.assertEqual(resource_info, {"url": "mcp://tool/financial_analysis"})

    def test_non_string_non_dict_resource_rejected(self):
        c = clone(SPEC_CHALLENGE["result"]["structuredContent"])
        c["resource"] = 42
        with self.assertRaisesRegex(x402_pay.CeremonyError, "resource"):
            x402_pay.parse_mcp_challenge(c)

    def test_non_dict_extra_fails_validation_not_crash(self):
        c = clone(SPEC_CHALLENGE["result"]["structuredContent"])
        c["accepts"][0]["extra"] = None
        options, _, _ = x402_pay.parse_mcp_challenge(c)
        option = x402_pay.select(options)
        with self.assertRaisesRegex(x402_pay.CeremonyError, "name/version"):
            x402_pay.validate(option, option["chainId"])

    def test_rejects_non_challenge_result(self):
        result = {"isError": True, "content": [{"type": "text", "text": "tool exploded"}]}
        with self.assertRaisesRegex(x402_pay.CeremonyError, "not an x402 payment challenge"):
            x402_pay.parse_mcp_challenge({"jsonrpc": "2.0", "id": 1, "result": result})

    def test_rejects_non_dict(self):
        with self.assertRaises(x402_pay.CeremonyError):
            x402_pay.parse_mcp_challenge([1, 2, 3])


class PaymentPayloadConformanceTest(unittest.TestCase):
    """build_payment() must produce the spec's exact _meta["x402/payment"] object."""

    def setUp(self):
        seed_asset_meta()

    def test_payload_matches_spec_retry_vector(self):
        options, resource_info, _ = x402_pay.parse_mcp_challenge(SPEC_CHALLENGE)
        option = x402_pay.select(options)
        x402_pay.validate(option, option["chainId"])
        spec_payload = SPEC_PAYMENT["payload"]
        payment = x402_pay.build_payment(
            2,
            option,
            resource_info,
            spec_payload["signature"],
            spec_payload["authorization"],
            None,
        )
        self.assertEqual(payment, SPEC_PAYMENT)

    def test_option_is_eligible_and_described(self):
        options, _, _ = x402_pay.parse_mcp_challenge(SPEC_CHALLENGE)
        option = x402_pay.select(options)
        self.assertTrue(option["eligible"])
        self.assertEqual(option["chainId"], 84532)
        self.assertEqual(option["assetTransferMethod"], "eip3009")
        self.assertEqual(option["humanAmount"], "0.01")

    def test_multiple_eligible_options_need_disambiguation(self):
        challenge = clone(SPEC_CHALLENGE["result"]["structuredContent"])
        second = clone(challenge["accepts"][0])
        second["network"] = "eip155:8453"
        challenge["accepts"].append(second)
        x402_pay._asset_meta_cache[(8453, second["asset"].lower())] = {
            "symbol": "USDC",
            "decimals": 6,
        }
        options, _, _ = x402_pay.parse_mcp_challenge(challenge)
        with self.assertRaisesRegex(x402_pay.CeremonyError, "multiple eligible"):
            x402_pay.select(options)
        picked = x402_pay.select(options, want_network="eip155:8453")
        self.assertEqual(picked["network"], "eip155:8453")


class ReadChallengeTest(unittest.TestCase):
    def test_inline_json(self):
        self.assertEqual(x402_pay.read_challenge('{"a": 1}', None), {"a": 1})

    def test_file(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(SPEC_CHALLENGE, f)
            path = f.name
        try:
            self.assertEqual(x402_pay.read_challenge(None, path), SPEC_CHALLENGE)
        finally:
            os.unlink(path)

    def test_both_sources_rejected(self):
        with self.assertRaisesRegex(x402_pay.CeremonyError, "not both"):
            x402_pay.read_challenge("{}", "some-file.json")

    def test_empty_challenge_with_file_still_rejected(self):
        # An unset shell variable must not silently defer to the other source.
        with self.assertRaisesRegex(x402_pay.CeremonyError, "not both"):
            x402_pay.read_challenge("", "some-file.json")

    def test_empty_challenge_string(self):
        with self.assertRaisesRegex(x402_pay.CeremonyError, "empty"):
            x402_pay.read_challenge("", None)

    def test_no_source_errors_instead_of_reading_stdin(self):
        # Agent harnesses keep a non-TTY pipe open on stdin; an implicit stdin
        # fallback would block forever on a forgotten flag.
        with self.assertRaisesRegex(x402_pay.CeremonyError, "no challenge given"):
            x402_pay.read_challenge(None, None)

    def test_missing_file(self):
        with self.assertRaisesRegex(x402_pay.CeremonyError, "challenge-file"):
            x402_pay.read_challenge(None, "/nonexistent/challenge.json")

    def test_invalid_json(self):
        with self.assertRaisesRegex(x402_pay.CeremonyError, "not valid JSON"):
            x402_pay.read_challenge("{nope", None)

    def test_empty_stdin(self):
        with mock.patch("sys.stdin", io.StringIO("")):
            with self.assertRaisesRegex(x402_pay.CeremonyError, "empty"):
                x402_pay.read_challenge("-", None)

    def test_stdin_json(self):
        with mock.patch("sys.stdin", io.StringIO(json.dumps(SPEC_CHALLENGE))):
            self.assertEqual(x402_pay.read_challenge("-", None), SPEC_CHALLENGE)


class CliTest(unittest.TestCase):
    def setUp(self):
        seed_asset_meta()

    def test_mcp_inspect_prints_options(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = x402_pay.main(["mcp-inspect", "--challenge", json.dumps(SPEC_CHALLENGE)])
        self.assertEqual(rc, 0)
        report = json.loads(out.getvalue())
        self.assertEqual(report["status"], "payment_required")
        self.assertEqual(report["x402Version"], 2)
        self.assertEqual(report["resource"]["url"], "mcp://tool/financial_analysis")
        self.assertEqual(report["options"][0]["humanAmount"], "0.01")

    def test_mcp_sign_refuses_without_confirm(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = x402_pay.main(["mcp-sign", "--challenge", json.dumps(SPEC_CHALLENGE)])
        self.assertEqual(rc, 1)
        report = json.loads(err.getvalue())
        self.assertEqual(report["status"], "error")
        self.assertIn("--confirm", report["error"])

    def test_mcp_inspect_rejects_v1(self):
        v1 = clone(SPEC_CHALLENGE["result"]["structuredContent"])
        v1["x402Version"] = 1
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = x402_pay.main(["mcp-inspect", "--challenge", json.dumps(v1)])
        self.assertEqual(rc, 1)
        self.assertIn("v2 only", json.loads(err.getvalue())["error"])

    def test_mcp_sign_fails_closed_without_resource(self):
        # No resource -> refuse BEFORE any mm call, instead of signing a real
        # authorization and emitting a payload with "resource": {"url": null}.
        c = clone(SPEC_CHALLENGE["result"]["structuredContent"])
        del c["resource"]
        err = io.StringIO()
        with mock.patch.object(
            x402_pay, "wallet_address", side_effect=AssertionError("mm was called")
        ):
            with contextlib.redirect_stderr(err):
                rc = x402_pay.main(["mcp-sign", "--challenge", json.dumps(c), "--confirm"])
        self.assertEqual(rc, 1)
        self.assertIn("resource", json.loads(err.getvalue())["error"])


if __name__ == "__main__":
    unittest.main()
