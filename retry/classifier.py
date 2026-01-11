def classify_failure(error_code: str) -> str:
    if error_code in ("TIMEOUT", "CONNECTION_RESET"):
        return "TRANSIENT"

    if error_code in ("429", "RATE_LIMIT"):
        return "RATE_LIMITED"

    if error_code.startswith("5"):
        return "SYSTEMIC"

    return "PERMANENT"
