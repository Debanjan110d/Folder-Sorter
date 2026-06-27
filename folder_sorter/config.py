import json
import os
from pathlib import Path

# Default file extension categories
DEFAULT_CONFIG = {
    "categories": {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
        "Audio": [".mp3", ".wav", ".flac", ".aac"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Code": [".py", ".js", ".ts", ".cpp", ".c", ".java", ".html", ".css"]
    }
}

def get_app_dir() -> Path:
    """Get the global application folder path (~/.folder-sorter)."""
    app_dir = Path.home() / ".folder-sorter"
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir

def get_config_file() -> Path:
    """Get the configuration file path."""
    return get_app_dir() / "config.json"

def load_config() -> dict:
    """Load configuration from ~/.folder-sorter/config.json, creating it with defaults if missing."""
    config_file = get_config_file()
    if not config_file.exists():
        try:
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
        except Exception:
            return DEFAULT_CONFIG
        return DEFAULT_CONFIG
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CONFIG

# Dynamic configuration state loaded at package initialization
config_data = load_config()
categories = config_data.get("categories", DEFAULT_CONFIG["categories"])

# Expose category sets for fast inclusion lookups
IMAGE_EXTENSIONS = set(categories.get("Images", DEFAULT_CONFIG["categories"]["Images"]))
VIDEO_EXTENSIONS = set(categories.get("Videos", DEFAULT_CONFIG["categories"]["Videos"]))
AUDIO_EXTENSIONS = set(categories.get("Audio", DEFAULT_CONFIG["categories"]["Audio"]))
DOCUMENT_EXTENSIONS = set(categories.get("Documents", DEFAULT_CONFIG["categories"]["Documents"]))
ARCHIVE_EXTENSIONS = set(categories.get("Archives", DEFAULT_CONFIG["categories"]["Archives"]))
CODE_EXTENSIONS = set(categories.get("Code", DEFAULT_CONFIG["categories"]["Code"]))

def save_config(categories_dict: dict) -> bool:
    """Save category config back to the global json file."""
    config_file = get_config_file()
    try:
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump({"categories": categories_dict}, f, indent=4)
        return True
    except Exception:
        return False