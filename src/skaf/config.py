from pathlib import Path
import os

import sys
import shutil

APP_NAME = "skaf"

def get_config_dir() -> Path:
    if sys.platform == "win32":
        # Windows: %APPDATA%\skaf
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        return base / APP_NAME
    else:
        # Linux/macOS: ~/.config/skaf
        return Path.home() / ".config" / APP_NAME

CONFIG_DIR = get_config_dir()
GLOBAL_TEMPLATES_DIR = CONFIG_DIR / "templates"
LOCAL_TEMPLATES_DIR = Path(__file__).parent / "templates"

def ensure_templates_exist():
    """Bootstrap: Copy bundled templates to global config if global is empty."""
    os.makedirs(GLOBAL_TEMPLATES_DIR, exist_ok=True)
    
    # If global templates dir is empty, copy from local
    if not any(GLOBAL_TEMPLATES_DIR.iterdir()) and LOCAL_TEMPLATES_DIR.exists():
        for item in LOCAL_TEMPLATES_DIR.iterdir():
            if item.is_dir():
                dest = GLOBAL_TEMPLATES_DIR / item.name
                if not dest.exists():
                    shutil.copytree(item, dest)

def get_templates_directories():
    ensure_templates_exist()
    dirs = [GLOBAL_TEMPLATES_DIR, LOCAL_TEMPLATES_DIR]
    return [d for d in dirs if d.exists()]
