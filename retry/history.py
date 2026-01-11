import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("logs/retry_log.ndjson")
LOG_FILE.parent.mkdir(exist_ok=True)

def log_event(event: dict):
    event["timestamp"] = datetime.utcnow().isoformat()

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")
