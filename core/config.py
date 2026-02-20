import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "download_path": os.getcwd(),
    "theme": "dark",
    "language": "ru",
    "auto_update": True
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG
    with open(CONFIG_FILE) as f:
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)