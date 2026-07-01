import json
import logging
import os
from datetime import datetime, timedelta

CHECKPOINT_FILE = "checkpoint.json"
CHECKPOINT_TTL_HOURS = 1


def save_checkpoint(page: int, saved_total: int):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump({
            "page": page,
            "saved_total": saved_total,
            "timestamp": datetime.now().isoformat()
        }, f)


def clear_checkpoint():
    logging.info("Clearing checkpoint")
    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)


def load_checkpoint() -> tuple[int, int]:
    if not os.path.exists(CHECKPOINT_FILE):
        return 2, 0

    with open(CHECKPOINT_FILE) as f:
        data = json.load(f)

    saved_at = datetime.fromisoformat(data["timestamp"])
    if datetime.now() - saved_at > timedelta(hours=CHECKPOINT_TTL_HOURS):
        logging.info("Checkpoint expired, starting fresh")
        clear_checkpoint()
        return 1, 0

    logging.info(f"Resuming from page {data['page']}")
    return data["page"], data["saved_total"]