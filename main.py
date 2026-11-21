import importlib
import logging
import os
import sys
from pathlib import Path

from config import APP_NAME, HOST_PORT, RECEIVED_DIR, TEMP_DIR, ensure_directories
from backend.network import get_network_info
from backend.server import create_app


def setup_logging() -> logging.Logger:
    logger = logging.getLogger("shivshare")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%H:%M:%S"))
        logger.addHandler(handler)
    return logger


def check_dependencies(logger: logging.Logger) -> bool:
    """Verify required Python packages are installed."""
    missing = []
    for pkg in ("flask", "werkzeug", "sqlite3"):
        try:
            importlib.import_module(pkg)
        except ImportError:
            missing.append(pkg)

    if missing:
        logger.error("Missing required Python modules: %s", ", ".join(missing))
        logger.error("Run: pip install -r requirements.txt")
        return False
    return True


def check_storage_permissions(logger: logging.Logger) -> bool:
    """Ensure storage directories exist and are writable; warn if Termux shared storage is unlinked."""
    try:
        ensure_directories()
    except OSError as exc:
        logger.error("Failed to create storage directories: %s", exc)
        return False

    for path in (RECEIVED_DIR, TEMP_DIR):
        if not (os.access(path, os.R_OK) and os.access(path, os.W_OK)):
            logger.error("Insufficient read/write permissions for directory: %s", path)
            return False

    termux_shared = Path.home() / "storage" / "shared"
    if not termux_shared.exists():
        logger.warning(
            "Termux shared storage link (~/storage/shared) not found. "
            "Run 'termux-setup-storage' in Termux to access shared Android folders."
        )
    return True


def print_banner(ip: str, port: int, network_type: str, pin: str) -> None:
    url = f"http://{ip}:{port}"
    print("=" * 40)
    print(f"       {APP_NAME} SERVER")
    print("=" * 40)
    print()
    print("Status: RUNNING")
    print()
    print("Local URL:")
    print(url)
    print()
    print(f"Port: {port}")
    print(f"Network: {network_type}")
    print(f"Pairing PIN: {pin}")
    print("Internet: Not Required")
    print()
    print("Waiting for devices...")
    print()
    print("=" * 40)


def main() -> int:
    logger = setup_logging()

    if not check_dependencies(logger):
        return 1

    if not check_storage_permissions(logger):
        return 1

    net_info = get_network_info(port=HOST_PORT)
    local_ip = str(net_info["local_ip"])
    network_type = str(net_info["network_type"])

    app = create_app(port=HOST_PORT)
    sec = app.extensions["shivshare"]["security"]
    pin = sec.get_pin()

    print_banner(ip=local_ip, port=HOST_PORT, network_type=network_type, pin=pin)

    if local_ip == "127.0.0.1":
        logger.warning(
            "No LAN/Hotspot IPv4 address detected. Connect to a Wi-Fi network or enable Mobile Hotspot."
        )
    logger.info("%s", net_info["ap_isolation_note"])

    bind_host = local_ip if local_ip != "127.0.0.1" else "0.0.0.0"

    try:
        app.run(host=bind_host, port=HOST_PORT, threaded=True, use_reloader=False)
    except OSError as exc:
        logger.error("Could not bind server on %s:%s — %s", bind_host, HOST_PORT, exc)
        logger.error("Check if port %s is already in use or try another Wi-Fi/hotspot interface.", HOST_PORT)
        return 1
    except KeyboardInterrupt:
        print("\nStopping SHIVSHARE LAN server...")
    return 0


if __name__ == "__main__":
    sys.exit(main())