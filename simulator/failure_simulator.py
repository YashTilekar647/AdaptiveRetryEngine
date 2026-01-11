import random

def simulate_failure():
    return random.choice([
        "TIMEOUT",
        "CONNECTION_RESET",
        "500",
        "429",
        "400"
    ])
