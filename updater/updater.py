# updater/updater.py
import sys
import os
import hashlib
import tempfile
import requests
import subprocess

def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def download(url: str, out_path: str):
    r = requests.get(url, stream=True, timeout=30)
    r.raise_for_status()
    with open(out_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

def main():
    # Ожидаем: updater.exe <url_to_setup> <sha256_expected>
    if len(sys.argv) < 3:
        print("Usage: updater.exe <url> <sha256>")
        sys.exit(2)

    url = sys.argv[1]
    expected = sys.argv[2].lower().strip()

    tmp_setup = os.path.join(tempfile.gettempdir(), "UltimateDownloader_update_setup.exe")

    print("Downloading setup...")
    download(url, tmp_setup)

    print("Verifying SHA256...")
    got = sha256(tmp_setup).lower()
    if got != expected:
        print("SHA256 mismatch!")
        sys.exit(3)

    print("Running installer silently...")
    # /VERYSILENT ставит поверх старой версии (если AppId тот же)
    subprocess.Popen([tmp_setup, "/VERYSILENT", "/NORESTART"], close_fds=True)

if __name__ == "__main__":
    main()