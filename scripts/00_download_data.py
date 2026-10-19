#!/usr/bin/env python3
"""
scripts/00_download_data.py
Downloads the published Supplementary Data 01 & 02 from npj Microgravity (Ferl et al., 2026)
and fetches comparative datasets from NASA OSDR (OSD-624 / VG Unity 22).
"""
import os
import sys
import json
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

URLS = {
    "41526_2026_645_MOESM1_ESM.xlsx": (
        "https://media.springernature.com/original/springer-static/esm/"
        "art%3A10.1038%2Fs41526-026-00645-6/MediaObjects/41526_2026_645_MOESM1_ESM.xlsx"
    ),
    "41526_2026_645_MOESM2_ESM.xlsx": (
        "https://media.springernature.com/original/springer-static/esm/"
        "art%3A10.1038%2Fs41526-026-00645-6/MediaObjects/41526_2026_645_MOESM2_ESM.xlsx"
    )
}

def download_supplements():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"
    }
    for filename, url in URLS.items():
        dest = RAW_DIR / filename
        if dest.exists() and dest.stat().st_size > 1000:
            print(f"[SKIP] {filename} already exists ({dest.stat().st_size} bytes).")
            continue
        print(f"[DOWNLOADING] {filename} from {url}...")
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        with open(dest, "wb") as f:
            f.write(resp.content)
        print(f"[DONE] Saved {filename} ({len(resp.content)} bytes).")

def download_osd624():
    dest_meta = RAW_DIR / "OSD-624_metadata.json"
    dest_files = RAW_DIR / "OSD-624_files.json"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    for url, dest in [
        ("https://osdr.nasa.gov/osdr/data/osd/meta/624", dest_meta),
        ("https://osdr.nasa.gov/osdr/data/osd/files/624", dest_files)
    ]:
        if not dest.exists():
            print(f"[FETCHING] {dest.name} from {url}...")
            try:
                resp = requests.get(url, headers=headers, timeout=30)
                resp.raise_for_status()
                with open(dest, "w") as f:
                    f.write(resp.text)
                print(f"[DONE] Saved {dest.name}.")
            except Exception as e:
                print(f"[ERROR] Failed fetching {url}: {e}")
        else:
            print(f"[SKIP] {dest.name} already exists.")

if __name__ == "__main__":
    download_supplements()
    download_osd624()
