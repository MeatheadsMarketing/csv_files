#!/usr/bin/env python3
"""
download_csv.py — Clarity Hack (v1.1.1)

Compatible with Python 3.7 – 3.11.
Fetch a CSV from a URL and save it under
~/Downloads/full_stack_dev_tools/   (folder auto‑created).
If the request returns HTTP 403 (e.g. a private ChatGPT link), the script
opens the URL in your default browser so you can download manually.

Usage:
    python3 download_csv.py <csv_url> [output_name]
"""

import sys
import os
import webbrowser
import requests
from datetime import datetime
from typing import Optional
import unittest

DEST_DIR = os.path.expanduser("~/Downloads/full_stack_dev_tools")
os.makedirs(DEST_DIR, exist_ok=True)

def ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def out_path(name_or_none: Optional[str], url: str) -> str:
    """Return the final file path inside DEST_DIR."""
    fname = os.path.basename(name_or_none or url.split("?")[0] or "download.csv")
    return os.path.join(DEST_DIR, fname)

def download(url: str, target: Optional[str] = None) -> str:
    path = out_path(target, url)
    print(f"[{ts()}] ⬇️  Downloading {url} → {path} …")
    try:
        r = requests.get(url, timeout=30, headers={"User-Agent": "curl/8"})
        r.raise_for_status()
        with open(path, "wb") as fh:
            fh.write(r.content)
        print(f"[{ts()}] ✅ Saved to {path}")
    except requests.HTTPError as e:
        if e.response.status_code == 403:
            print(f"[{ts()}] 🔒 403 Forbidden — opening in browser …")
            webbrowser.open(url)
            path = ""
        else:
            print(f"[{ts()}] ❌ Download failed: {e}")
            path = ""
    except Exception as err:
        print(f"[{ts()}] ❌ Download failed: {err}")
        path = ""
    return path

# ────────────────────────────  TESTS  ────────────────────────────
class _Tests(unittest.TestCase):
    def test_out_path_derives_name(self):
        self.assertTrue(out_path(None, "https://x/y/z.csv").endswith("z.csv"))

    def test_out_path_custom_name(self):
        self.assertTrue(out_path("renamed.csv", "https://x/y/z.csv").endswith("renamed.csv"))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUsage: python3 download_csv.py <csv_url> [output_name]\n")
        sys.exit(1)

    download(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
