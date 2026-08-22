#!/usr/bin/env python3
"""Export canonical HTML to PDF and enforce basic page/render gates."""

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def runtime_config():
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    path = codex_home / "jizhi-runtime/runtime.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def ensure_runtime_python():
    if importlib.util.find_spec("pypdf"):
        return
    python = runtime_config().get("python")
    if python and Path(python).exists() and Path(python).absolute() != Path(sys.executable).absolute():
        os.execv(python, [python, __file__, *sys.argv[1:]])
    raise SystemExit("pypdf is missing. Run the package install.sh to configure the Jizhi runtime.")


def find_browser():
    configured = os.environ.get("JIZHI_CHROMIUM_PATH") or runtime_config().get("browser")
    if configured and Path(configured).exists():
        return configured
    candidates = (
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "google-chrome", "chromium", "chromium-browser",
    )
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return str(path)
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    raise SystemExit("No supported Chromium browser found for PDF export.")


def page_count(path):
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise SystemExit("pypdf is required for PDF verification.") from exc
    reader = PdfReader(str(path))
    return len(reader.pages)


def main():
    ensure_runtime_python()
    parser = argparse.ArgumentParser()
    parser.add_argument("input_html")
    parser.add_argument("output_pdf")
    parser.add_argument("--max-pages", type=int)
    args = parser.parse_args()
    source = Path(args.input_html).resolve()
    output = Path(args.output_pdf).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [find_browser(), "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={output}", source.as_uri()]
    subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if not output.exists() or output.stat().st_size < 1000:
        raise SystemExit("PDF export produced no usable file.")
    pages = page_count(output)
    if pages < 1:
        raise SystemExit("PDF has no pages.")
    if args.max_pages and pages > args.max_pages:
        raise SystemExit(f"PDF page count {pages} exceeds contract limit {args.max_pages}.")
    print(f"{output} pages={pages}")


if __name__ == "__main__":
    main()
