#!/usr/bin/env python3
"""Export canonical HTML to PDF and enforce basic page/render gates."""

import argparse
import shutil
import subprocess
from pathlib import Path


def find_browser():
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
