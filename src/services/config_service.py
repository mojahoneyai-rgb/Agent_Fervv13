"""
Configuration Service
Manages application settings, persistence, and defaults.
"""
import json
import os
from src.core.event_bus import global_event_bus

class ConfigService:
    def __init__(self, settings_file="settings.json"):
        self.settings_file = settings_file
        self.config = self._load()

    def _load(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save()
        global_event_bus.publish("config_changed", {"key": key, "value": value})

    def save(self):
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Config save error: {e}")
