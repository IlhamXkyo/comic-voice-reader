import os
import json
from .models import ReadingZone

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".comic_voice_reader")
CONFIG_PATH = os.path.join(CONFIG_DIR, "settings.json")

DEFAULT_CONFIG = {
    "reading_zone": {
        "x": 350,
        "y": 100,
        "width": 650,
        "height": 850
    },
    "voice_index": 0,  # 0: Instan Offline 0ms (Default Cepat!), 1: Ardi, 2: Gadis, 3: Brian
    "speed": 1.1,      # 0.75x to 2.0x
    "volume": 1.0,     # 0.0 to 1.0
    "scroll_debounce_ms": 100, # 100ms ultra responsif
    "similarity_threshold": 0.80,
    "auto_read_enabled": True
}

AVAILABLE_VOICES = [
    {
        "id": "local-sapi",
        "name": "⚡ Instan 0ms (Lokal Offline Tanpa Jeda)",
        "desc": "Suara lokal Windows langsung berbunyi seketika tanpa jeda internet",
        "lang": "id-ID",
        "type": "sapi"
    },
    {
        "id": "id-ID-ArdiNeural",
        "name": "🌐 Pria Natural (Ardi - Cloud)",
        "desc": "Suara pria natural bahasa Indonesia (Butuh Internet Cepat)",
        "lang": "id-ID",
        "type": "edge"
    },
    {
        "id": "id-ID-GadisNeural",
        "name": "🌐 Wanita Natural (Gadis - Cloud)",
        "desc": "Suara wanita jernih bahasa Indonesia (Butuh Internet Cepat)",
        "lang": "id-ID",
        "type": "edge"
    },
    {
        "id": "en-US-BrianNeural",
        "name": "🌐 Narator (Brian - Cloud)",
        "desc": "Suara narator ekspresif untuk dialog Inggris/Campuran",
        "lang": "en-US",
        "type": "edge"
    }
]

def load_config():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                config = DEFAULT_CONFIG.copy()
                config.update(data)
                return config
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(config_data):
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Gagal menyimpan konfigurasi: {e}")
