import json
import os

class SettingsManager:
    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.default_settings = {
            "feeds": [],  # List of dicts: {"url": ..., "category": ...}
            "refresh_interval": 15,  # minutes
            "dark_mode": False
        }

    def load_settings(self):
        if not os.path.exists(self.filename):
            return self.default_settings.copy()
        try:
            with open(self.filename, "r") as f:
                settings = json.load(f)
            # Merge with defaults in case of missing keys
            for key, value in self.default_settings.items():
                settings.setdefault(key, value)
            return settings
        except Exception:
            return self.default_settings.copy()

    def save_settings(self, settings):
        try:
            with open(self.filename, "w") as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")
			
	def update_feeds(feeds):
		settings = load_settings()
		settings['feeds'] = feeds
		save_settings(settings)

	def update_refresh_interval(interval):
		settings = load_settings()
		settings['refresh_interval'] = interval
		save_settings(settings)

	def update_theme(theme):
		settings = load_settings()
		settings['theme'] = theme
		save_settings(settings)
