#!/usr/bin/env python3
"""
scripts/01_poll_repositories.py
Polls NASA OSDR (OSD-948) and NCBI GEO (GSE312580) to detect when the
embargo lifts and data becomes publicly downloadable.
Can be run once or as a continuous watcher with configurable intervals.
"""
import os
import sys
import time
import json
import logging
from datetime import datetime
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = BASE_DIR / "data" / "raw"

log_file = LOG_DIR / "repository_watcher.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

OSDR_META_URL = "https://osdr.nasa.gov/osdr/data/osd/meta/948"
OSDR_FILES_URL = "https://osdr.nasa.gov/osdr/data/osd/files/948"
GEO_EUTILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term=GSE312580%5BACCN%5D&retmode=json"

def check_osdr():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(OSDR_META_URL, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            hits = data.get("hits", 0)
            if hits > 0:
                logging.info(f"🎉 OSD-948 IS PUBLIC ON OSDR! Hits: {hits}")
                return True, data
            else:
                logging.info(f"⏳ OSD-948 is still pending indexing on OSDR (hits: 0).")
                return False, data
        else:
            logging.warning(f"OSDR responded with status {resp.status_code}")
            return False, None
    except Exception as e:
        logging.warning(f"Error querying OSDR: {e}")
        return False, None

def check_geo():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(GEO_EUTILS_URL, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            count = int(data.get("esearchresult", {}).get("count", 0))
            if count > 0:
                id_list = data.get("esearchresult", {}).get("idlist", [])
                logging.info(f"🎉 GSE312580 IS PUBLIC ON NCBI GEO! IDs: {id_list}")
                return True, data
            else:
                logging.info("⏳ GSE312580 is still private/embargoed on NCBI GEO.")
                return False, data
        else:
            logging.warning(f"NCBI responded with status {resp.status_code}")
            return False, None
    except Exception as e:
        logging.warning(f"Error querying NCBI GEO: {e}")
        return False, None

def poll_once():
    logging.info("--- Starting Repository Poll ---")
    osdr_public, osdr_data = check_osdr()
    geo_public, geo_data = check_geo()
    
    status_file = LOG_DIR / "repository_status.json"
    with open(status_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "osdr_948_public": osdr_public,
            "geo_312580_public": geo_public,
            "osdr_data": osdr_data,
            "geo_data": geo_data
        }, f, indent=2)
    logging.info(f"Status recorded to {status_file}")
    return osdr_public or geo_public

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--watch":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 3600
        logging.info(f"Starting continuous watcher mode (interval: {interval}s)...")
        while True:
            released = poll_once()
            if released:
                logging.info("One or more repositories are now live! Triggering alert.")
                break
            time.sleep(interval)
    else:
        poll_once()
