#!/usr/bin/env python3
"""Call the separately installed private planning-pricing add-on."""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json")
    parser.add_argument("output_json")
    args = parser.parse_args()
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    calculator = codex_home / "skills/jizhi-planning-pricing-private/scripts/calculate_quote.py"
    if not calculator.exists():
        raise SystemExit("Private planning pricing add-on is not installed; output must remain 待内部核价.")
    subprocess.run([sys.executable, str(calculator), args.input_json, args.output_json], check=True)


if __name__ == "__main__":
    main()
