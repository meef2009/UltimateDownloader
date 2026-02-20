import os
import json

APP_NAME = "UltimateDownloader"

def get_config_path():
    base_dir = os.path.join(
        os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
        APP_NAME
    )
    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, "config.json")

def load_config():
    path = get_config_path()

    if not os.path.exists(path):
        default_config = {
            "language": "en",
            "download_path": os.path.join(os.path.expanduser("~"), "Downloads")
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4)
        return default_config

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    path = get_config_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)