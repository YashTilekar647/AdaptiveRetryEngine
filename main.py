from retry.engine import RetryEngine
from simulator.failure_simulator import simulate_failure

engine = RetryEngine()

for attempt in range(1, 15):
    error = simulate_failure()
    print(f"\nAttempt {attempt} failed with {error}")
    if not engine.attempt_retry(error, attempt):
        break

print("\n📊 Failure Summary")
print(engine.history.summary())
