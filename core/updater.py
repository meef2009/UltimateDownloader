import os
import sys
import requests
import subprocess
from version import VERSION

# ВСТАВЬ СЮДА ССЫЛКУ НА RAW latest.json
LATEST_JSON_URL = "https://raw.githubusercontent.com/meef2009/UltimateDownloader/refs/heads/main/latest.json"


def parse_version(v: str):
    return tuple(int(x) for x in v.strip().split("."))


def fetch_latest():
    r = requests.get(LATEST_JSON_URL, timeout=10)
    r.raise_for_status()
    data = r.json()
    return data["version"], data["setup_url"], data["sha256"]


def is_update_available(latest: str) -> bool:
    try:
        return parse_version(latest) > parse_version(VERSION)
    except:
        return False


def get_app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(""))


def start_update(setup_url: str, sha256: str) -> bool:
    app_dir = get_app_dir()
    updater_path = os.path.join(app_dir, "UltimateDownloaderUpdater.exe")

    if not os.path.exists(updater_path):
        return False

    subprocess.Popen([updater_path, setup_url, sha256], close_fds=True)
    return True