"""
sync_greetings.py
Keeps two greetings.xml files in sync.
The original is the source of truth — any change is copied to the destination.
Run this script in the background (or as a Windows service / scheduled task).
"""

import shutil
import time
import os
import logging
from datetime import datetime

# ── Paths ────────────────────────────────────────────────────────────────────
ORIGINAL = r"C:\Users\Administrator\AppData\Roaming\sb0t\sb0t.exe\greetings.xml"
COPY     = r"C:\Users\Administrator\AppData\Roaming\sb0t\sb0t.exe\Scripting\bienvenida.js\Data\greetings.xml"

# How often to check for changes (seconds)
CHECK_INTERVAL = 5

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),                                        # console
        logging.FileHandler("sync_greetings.log", "a", encoding="utf-8"),  # log file
    ],
)
log = logging.getLogger(__name__)


def get_mtime(path: str) -> float:
    """Return last-modified timestamp, or -1 if file doesn't exist."""
    try:
        return os.path.getmtime(path)
    except FileNotFoundError:
        return -1.0


def files_are_identical(a: str, b: str) -> bool:
    """Quick size check first, then byte comparison."""
    try:
        if os.path.getsize(a) != os.path.getsize(b):
            return False
        with open(a, "rb") as fa, open(b, "rb") as fb:
            return fa.read() == fb.read()
    except OSError:
        return False


def sync_once() -> None:
    """Copy ORIGINAL → COPY if the original is newer or content differs."""
    if not os.path.exists(ORIGINAL):
        log.warning("Original file not found: %s", ORIGINAL)
        return

    dest_dir = os.path.dirname(COPY)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)
        log.info("Created missing destination directory: %s", dest_dir)

    orig_mtime = get_mtime(ORIGINAL)
    copy_mtime = get_mtime(COPY)

    # Copy when: copy doesn't exist, original is newer, or content differs
    needs_update = (
        copy_mtime == -1.0          # copy missing
        or orig_mtime > copy_mtime  # original was modified after copy
        or not files_are_identical(ORIGINAL, COPY)  # content mismatch
    )

    if needs_update:
        shutil.copy2(ORIGINAL, COPY)   # copy2 preserves timestamps
        log.info("Synced  ->  %s", COPY)
    else:
        log.debug("Files are identical — nothing to do.")


def main() -> None:
    log.info("=== greetings.xml sync started ===")
    log.info("Source : %s", ORIGINAL)
    log.info("Dest   : %s", COPY)
    log.info("Interval: %ds", CHECK_INTERVAL)

    while True:
        try:
            sync_once()
        except Exception as exc:
            log.error("Unexpected error during sync: %s", exc)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
