LANG = {
    "ru": {
        "download": "Скачать",
        "settings": "Настройки",
        "search": "Поиск",
        "login": "Вход"
    },
    "en": {
        "download": "Download",
        "settings": "Settings",
        "search": "Search",
        "login": "Login"
    }
}

def t(key, lang):
    return LANG.get(lang, LANG["ru"]).get(key, key)