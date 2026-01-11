import time
import json
from datetime import datetime

from retry.classifier import classify_failure
from retry.strategies import exponential_backoff, cooldown_backoff
from retry.circuit_breaker import CircuitBreaker
from retry.budget import RetryBudget
from retry.history import log_event   # ✅ FUNCTION-BASED LOGGING

LOG_FILE = "logs/retry_log.json"


class RetryEngine:
    def __init__(self):
        self.circuit = CircuitBreaker()
        self.budget = RetryBudget()

    def _log(self, payload: dict):
        payload["timestamp"] = datetime.now().isoformat()
        log_event(payload)

    def attempt_retry(self, error_type: str, attempt_number: int) -> bool:
        # 🚫 Circuit breaker check
        if self.circuit.open:
            self._log({"event": "circuit_open"})
            return False

        # 🚫 Retry budget check
        if not self.budget.consume():
            self._log({"event": "budget_exhausted"})
            return False

        # 🔍 Classify failure
        failure_type = classify_failure(error_type)

        # ❌ Permanent failures should NOT retry
        if failure_type == "PERMANENT":
            self._log({
                "event": "permanent_failure",
                "error": error_type,
                "failure_type": failure_type
            })
            return False

        # 🔄 Decide backoff strategy
        if failure_type == "SYSTEMIC":
            self.circuit.record_failure()
            delay = cooldown_backoff()
        else:
            delay = exponential_backoff(attempt_number)

        # 📝 Log retry
        self._log({
            "event": "retry",
            "error": error_type,
            "failure_type": failure_type,
            "delay": delay,
            "attempt": attempt_number
        })

        # ⏱ Simulated wait (keep small for demo)
        time.sleep(1)
        return True
