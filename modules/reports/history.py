"""Persistent, privacy-aware activity history for the local dashboard."""

import json
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
HISTORY_PATH = PROJECT_ROOT / "reports" / "activity_history.json"
MAX_RECORDS = 100


def _read_history():
    try:
        if HISTORY_PATH.exists():
            data = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        pass

    return []


def record_activity(module, target, status, summary, output=None):
    """Save a dashboard action. Callers must not include sensitive inputs."""
    history = _read_history()
    record = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "module": str(module),
        "target": str(target or "Local input"),
        "status": str(status),
        "summary": str(summary),
        "output": output if output is not None else {},
    }

    history.insert(0, record)
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_PATH.write_text(
        json.dumps(history[:MAX_RECORDS], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return record


def get_activity_history():
    """Return newest dashboard history first."""
    return _read_history()
