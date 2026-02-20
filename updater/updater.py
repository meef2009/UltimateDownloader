# updater/updater.py
# Production updater for UltimateDownloader
# Supports:
#   1) updater.exe <setup_url> <sha256>
#   2) updater.exe <latest_json_url>
#
# Features:
# - SHA256 verification
# - retries + timeouts
# - logs to %LOCALAPPDATA%\UltimateDownloader\logs\updater.log
# - silent install (Inno Setup): /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /CLOSEAPPLICATIONS
# - cleanup downloaded setup after launch

import sys
import os
import json
import time
import hashlib
import tempfile
import subprocess
from datetime import datetime

import requests


APP_NAME = "UltimateDownloader"


def appdata_dir() -> str:
    base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    p = os.path.join(base, APP_NAME)
    os.makedirs(p, exist_ok=True)
    return p


def log_path() -> str:
    p = os.path.join(appdata_dir(), "logs")
    os.makedirs(p, exist_ok=True)
    return os.path.join(p, "updater.log")


def log(msg: str):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    try:
        with open(log_path(), "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass
    print(line)


def show_error_box(title: str, message: str):
    # UI fallback (works even in --windowed builds)
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)  # MB_ICONERROR
    except Exception:
        pass


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().lower()


def http_get_json(url: str, timeout: int = 25, retries: int = 3) -> dict:
    last_err = None
    for i in range(retries):
        try:
            log(f"GET JSON: {url} (try {i+1}/{retries})")
            r = requests.get(url, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last_err = e
            wait = 1.5 * (i + 1)
            log(f"JSON fetch failed: {e}. retry in {wait:.1f}s")
            time.sleep(wait)
    raise last_err


def download_file(url: str, out_path: str, timeout: int = 60, retries: int = 3):
    last_err = None
    for i in range(retries):
        try:
            log(f"DOWNLOAD: {url} -> {out_path} (try {i+1}/{retries})")
            with requests.get(url, stream=True, timeout=timeout) as r:
                r.raise_for_status()
                total = int(r.headers.get("content-length", "0") or "0")
                got = 0
                with open(out_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
                            got += len(chunk)
                if os.path.getsize(out_path) == 0:
                    raise RuntimeError("Downloaded file is empty")
                if total and got < total:
                    raise RuntimeError(f"Incomplete download: {got}/{total}")
            return
        except Exception as e:
            last_err = e
            wait = 2.0 * (i + 1)
            log(f"Download failed: {e}. retry in {wait:.1f}s")
            time.sleep(wait)
    raise last_err


def parse_args():
    """
    Returns (setup_url, expected_sha, version_optional)
    """
    if len(sys.argv) < 2:
        raise SystemExit("Usage:\n  updater.exe <setup_url> <sha256>\n  updater.exe <latest_json_url>")

    # Mode A: updater.exe <latest_json_url>
    if len(sys.argv) == 2:
        latest_url = sys.argv[1]
        data = http_get_json(latest_url)
        setup_url = data.get("setup_url")
        expected = (data.get("sha256") or "").lower().strip()
        version = (data.get("version") or "").strip()
        if not setup_url or not expected:
            raise RuntimeError("latest.json missing setup_url/sha256")
        return setup_url, expected, version

    # Mode B: updater.exe <setup_url> <sha256>
    setup_url = sys.argv[1]
    expected = sys.argv[2].lower().strip()
    return setup_url, expected, ""


def run_installer(setup_path: str) -> int:
    # Inno Setup flags:
    # /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /CLOSEAPPLICATIONS
    args = [setup_path, "/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART", "/CLOSEAPPLICATIONS"]
    log("RUN INSTALLER: " + " ".join(args))
    try:
        p = subprocess.Popen(args, close_fds=True)
        return p.wait()
    except Exception as e:
        log(f"Installer start failed: {e}")
        return 999


def schedule_delete(path: str):
    # delete after a few seconds (installer may still have file open)
    try:
        cmd = f'timeout /t 5 >nul & del /f /q "{path}"'
        subprocess.Popen(["cmd", "/c", cmd], close_fds=True)
        log(f"Scheduled delete: {path}")
    except Exception:
        pass


def main():
    try:
        setup_url, expected_sha, ver = parse_args()
        log("==== Updater started ====")
        if ver:
            log(f"Target version: {ver}")
        log(f"Setup URL: {setup_url}")
        log(f"Expected SHA256: {expected_sha}")

        # temp file
        tmp_dir = tempfile.gettempdir()
        tmp_setup = os.path.join(tmp_dir, f"{APP_NAME}_update_setup.exe")

        # download
        download_file(setup_url, tmp_setup)

        # verify
        got = sha256_file(tmp_setup)
        log(f"SHA256 got: {got}")
        if got != expected_sha:
            log("SHA256 mismatch! Abort.")
            show_error_box("Update failed", "SHA256 mismatch. Update file may be corrupted.")
            schedule_delete(tmp_setup)
            sys.exit(3)

        # run installer and wait
        code = run_installer(tmp_setup)
        log(f"Installer exit code: {code}")

        schedule_delete(tmp_setup)

        if code != 0:
            show_error_box("Update failed", f"Installer finished with error code: {code}\nSee updater log in AppData.")
            sys.exit(code)

        log("Update finished OK.")
        sys.exit(0)

    except SystemExit as e:
        raise
    except Exception as e:
        log(f"FATAL: {e}")
        show_error_box("Updater error", f"{e}\nSee updater log in AppData.")
        sys.exit(10)


if __name__ == "__main__":
    main()