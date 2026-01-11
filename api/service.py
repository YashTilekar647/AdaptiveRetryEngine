from fastapi import FastAPI, HTTPException
import requests
import random
from retry.engine import RetryEngine

# --------------------------------
# App Setup
# --------------------------------

app = FastAPI(
    title="Adaptive Retry Service",
    description="Demonstrates adaptive retry logic for unreliable external APIs",
    version="1.0"
)

engine = RetryEngine()

MAX_ATTEMPTS = 5
REQUEST_TIMEOUT = 2  # seconds


# --------------------------------
# External API Simulator
# --------------------------------
def get_external_api():
    """
    Simulates real-world unstable external services
    """
    r = random.random()

    if r < 0.5:
        return "https://httpbin.org/status/200"     # Success
    elif r < 0.75:
        return "https://httpbin.org/status/500"     # Server error
    elif r < 0.9:
        return "https://httpbin.org/status/503"     # Service unavailable
    else:
        return "https://httpbin.org/delay/3"        # Timeout


# --------------------------------
# Root Endpoint
# --------------------------------
@app.get("/")
def home():
    return {
        "message": "Adaptive Retry Engine API is running",
        "usage": "Go to /docs and call /fetch-data"
    }


# --------------------------------
# Retry-enabled API Call
# --------------------------------
@app.get("/fetch-data")
def fetch_data():
    attempt = 1
    last_error = None

    while attempt <= MAX_ATTEMPTS:
        try:
            url = get_external_api()
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

            return {
                "status": "success",
                "attempts": attempt,
                "source_url": url
            }

        except requests.exceptions.Timeout:
            last_error = "TIMEOUT"

        except requests.exceptions.ConnectionError:
            last_error = "CONNECTION_RESET"

        except requests.exceptions.HTTPError as e:
            last_error = f"HTTP_{e.response.status_code}"

        # Ask retry engine if retry is allowed
        should_retry = engine.attempt_retry(
            error_type=last_error,
            attempt_number=attempt
        )

        if not should_retry:
            break

        attempt += 1

    # If all retries failed
    raise HTTPException(
        status_code=503,
        detail={
            "message": "Service unavailable after adaptive retries",
            "attempts": attempt - 1,
            "last_error": last_error
        }
    )
