"""Persistent, privacy-aware activity history for the local dashboard."""

import json
import os
import sys
import threading
from datetime import datetime
from pathlib import Path

_LOCK = threading.Lock()

if getattr(sys, "frozen", False):
    BASE_DIR = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "NightHunter"
else:
    BASE_DIR = Path(__file__).resolve().parents[2]

HISTORY_PATH = BASE_DIR / "reports" / "activity_history.json"
MAX_RECORDS = 100


def _read_history():
    with _LOCK:
        try:
            if HISTORY_PATH.exists():
                data = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
                return data if isinstance(data, list) else []
        except (OSError, json.JSONDecodeError):
            pass

    return []


def record_activity(module, target, status, summary, output=None):
    """Save a dashboard action atomically with thread safety. Callers must not include sensitive inputs."""
    record = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "module": str(module),
        "target": str(target or "Local input"),
        "status": str(status),
        "summary": str(summary),
        "output": output if output is not None else {},
    }

    with _LOCK:
        history = []
        try:
            if HISTORY_PATH.exists():
                data = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    history = data
        except (OSError, json.JSONDecodeError):
            history = []

        history.insert(0, record)
        HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = HISTORY_PATH.with_suffix(".tmp")
        tmp_path.write_text(
            json.dumps(history[:MAX_RECORDS], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        os.replace(tmp_path, HISTORY_PATH)

    return record


def get_activity_history():
    """Return newest dashboard history first."""
    return _read_history()
