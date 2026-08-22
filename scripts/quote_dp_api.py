#!/usr/bin/env python3
"""Backward-compatible entrypoint for the DP quote skill."""

from pathlib import Path
import runpy

SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "dp-product-new-customer-quote" / "scripts" / "quote_dp_api.py"
runpy.run_path(str(SCRIPT), run_name="__main__")
