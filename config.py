import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Network settings
HOST_PORT = 8080
BIND_ALL_INTERFACES = False  # Prefer detected LAN IP; fallback to 0.0.0.0 if needed

# Storage directories
STORAGE_DIR = BASE_DIR / "storage"
RECEIVED_DIR = STORAGE_DIR / "received"
TEMP_DIR = STORAGE_DIR / "temp"
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "shivshare.db"

# Optional Android Termux shared storage paths (checked safely at runtime)
ANDROID_SHARED_CANDIDATES = [
    Path.home() / "storage" / "shared" / "Download",
    Path.home() / "storage" / "shared" / "DCIM",
    Path.home() / "storage" / "shared" / "Pictures",
    Path.home() / "storage" / "shared" / "Music",
    Path.home() / "storage" / "shared" / "Movies",
    Path.home() / "storage" / "shared" / "Documents",
    Path("/sdcard/Download"),
    Path("/sdcard/DCIM"),
    Path("/sdcard/Pictures"),
    Path("/sdcard/Music"),
    Path("/sdcard/Movies"),
    Path("/sdcard/Documents"),
]

# Transfer & streaming settings (optimized for Termux RAM & storage)
CHUNK_SIZE = 256 * 1024  # 256 KB streaming chunks
MAX_FILE_SIZE_BYTES = 16 * 1024 * 1024 * 1024  # 16 GB ceiling check against free disk space
SPEED_WINDOW_SECONDS = 3.0  # Rolling window for smooth speed & ETA calculation
SESSION_TTL_SECONDS = 6 * 3600  # 6 hours
MAX_PIN_ATTEMPTS = 8
RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_REQUESTS = 240

# Security & Flask secret
APP_NAME = "SHIVSHARE LAN"
APP_VERSION = "1.0.0"
SECRET_KEY = os.environ.get("SHIVSHARE_SECRET_KEY") or secrets.token_hex(32)

# Categorization map for File Manager
FILE_CATEGORIES = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".heic", ".svg"},
    "videos": {".mp4", ".mkv", ".avi", ".mov", ".webm", ".3gp", ".m4v"},
    "audio": {".mp3", ".wav", ".ogg", ".m4a", ".flac", ".aac", ".opus"},
    "documents": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".csv", ".md"},
    "apk": {".apk"},
    "zip": {".zip", ".rar", ".7z", ".tar", ".gz", ".xz"},
}


def ensure_directories() -> None:
    """Create required runtime directories if they do not exist."""
    for directory in (STORAGE_DIR, RECEIVED_DIR, TEMP_DIR, DATABASE_DIR):
        directory.mkdir(parents=True, exist_ok=True)