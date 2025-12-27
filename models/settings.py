import json
import os

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "store_name": "DexKasir Store",
    "store_address": "Jl. Contoh No. 123, Jakarta",
    "tax_rate": 10.0,
    "printer_name": "Default Printer",
    "theme": "Dark"
}

class SettingsModel:
    def __init__(self):
        self.load_settings()

    def load_settings(self):
        if not os.path.exists(SETTINGS_FILE):
            self.settings = DEFAULT_SETTINGS.copy()
            self.save_settings()
        else:
            try:
                with open(SETTINGS_FILE, 'r') as f:
                    self.settings = json.load(f)
            except Exception:
                self.settings = DEFAULT_SETTINGS.copy()

    def save_settings(self):
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    def get(self, key):
        return self.settings.get(key, DEFAULT_SETTINGS.get(key))

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()
