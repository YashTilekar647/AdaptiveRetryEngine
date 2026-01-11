def exponential_backoff(attempt: int) -> int:
    return min(2 ** attempt, 60)

def cooldown_backoff() -> int:
    return 120
