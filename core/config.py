import os
import json

APP_NAME = "UltimateDownloader"
DEFAULT_CONFIG = {
    "theme": "dark",
    "language": "ru",
    "download_path": "",
}


def get_config_dir() -> str:
    # %APPDATA%\UltimateDownloader
    base = os.environ.get("APPDATA") or os.path.expanduser("~")
    return os.path.join(base, APP_NAME)


def get_config_path() -> str:
    return os.path.join(get_config_dir(), "config.json")


def load_config() -> dict:
    cfg_dir = get_config_dir()
    cfg_path = get_config_path()

    os.makedirs(cfg_dir, exist_ok=True)

    if not os.path.exists(cfg_path):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # на всякий случай подмешаем дефолты
        merged = DEFAULT_CONFIG.copy()
        merged.update(data if isinstance(data, dict) else {})
        return merged
    except Exception:
        # если файл битый — перезапишем дефолтом
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()


def save_config(cfg: dict) -> None:
    cfg_dir = get_config_dir()
    cfg_path = get_config_path()
    os.makedirs(cfg_dir, exist_ok=True)
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)