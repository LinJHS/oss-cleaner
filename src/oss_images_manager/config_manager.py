import json
import base64
import os
from pathlib import Path

class AppConfig:
    def __init__(self, app_name="oss-images-manager"):
        # Simple cross-platform path logic
        base_dir = Path(os.getenv('APPDATA') or Path.home() / ".config")
        self.config_dir = base_dir / app_name
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "settings.json"
        self.data = self._load()

    def _load(self):
        if self.config_file.exists():
            try:
                return json.loads(self.config_file.read_text(encoding='utf-8'))
            except Exception:
                return {}
        return {}

    def save(self):
        self.config_file.write_text(json.dumps(self.data, indent=4), encoding='utf-8')

    def get_secret(self, key):
        val = self.data.get(key)
        if val:
            try:
                return base64.b64decode(val.encode()).decode()
            except Exception:
                return None
        return None

    def set_secret(self, key, value):
        self.data[key] = base64.b64encode(value.encode()).decode()
        self.save()

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()
