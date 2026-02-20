import os, sys, shutil, hashlib, requests, subprocess, tempfile
from core import logger

APP_PATH = r"C:\Program Files\UltimateDownloader"
UPDATE_JSON = "https://yourserver.com/latest.json"

def sha256(file_path):
    h = hashlib.sha256()
    with open(file_path,"rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def download_file(url, dest):
    r = requests.get(url, stream=True)
    with open(dest,"wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)

def rollback(backup_path):
    shutil.copytree(backup_path, APP_PATH, dirs_exist_ok=True)
    logger.log("Rollback complete")

def main():
    data = requests.get(UPDATE_JSON).json()
    url = data["url"]
    expected_hash = data["sha256"]

    tmp_file = os.path.join(tempfile.gettempdir(),"update.tmp")
    download_file(url,tmp_file)

    if sha256(tmp_file) != expected_hash:
        logger.log("Hash mismatch! Abort update")
        sys.exit(1)

    backup = APP_PATH + "_backup"
    shutil.copytree(APP_PATH, backup, dirs_exist_ok=True)

    try:
        shutil.unpack_archive(tmp_file, APP_PATH)
    except:
        rollback(backup)
        sys.exit(1)

    subprocess.Popen(os.path.join(APP_PATH,"UltimateDownloader.exe"))

if __name__=="__main__":
    main()