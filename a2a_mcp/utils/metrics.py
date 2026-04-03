# utils/metrics.py

import time
import logging
from typing import Optional, Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("a2a_metrics")

class Metrics:
    def record(self, name: str, value: float, tags: Optional[Dict[str, Any]] = None):
        logger.info(f"[METRIC] {name}={round(value, 4)}s | tags={tags or {}}")

    def event(self, name: str, data: Dict[str, Any]):
        logger.info(f"[EVENT] {name} | {data}")

metrics = Metrics()