#!/usr/bin/env python3
"""Encode ERC-20 approve(address,uint256) calldata for an exact-amount allowance.

Usage:
    python3 encode_approve.py <spender_address> <amount> <decimals>

Examples:
    python3 encode_approve.py 0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2 100 6
    # approve 100 USDC (6 decimals) -> 0x095ea7b3000...0005f5e100
"""

import re
import sys
from decimal import Decimal

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <spender_address> <amount> <decimals>", file=sys.stderr)
    sys.exit(1)

spender = sys.argv[1]
if not re.fullmatch(r"0x[0-9a-fA-F]{40}", spender):
    print("error: spender must be a 0x-prefixed 40-hex-character address", file=sys.stderr)
    sys.exit(1)

decimals = int(sys.argv[3])
value = int(Decimal(sys.argv[2]) * 10 ** decimals)
if value < 0 or value >= 2 ** 256:
    print("error: amount out of uint256 range", file=sys.stderr)
    sys.exit(1)

selector = "095ea7b3"  # approve(address,uint256)
print("0x" + selector + spender[2:].lower().rjust(64, "0") + format(value, "x").rjust(64, "0"))
