class CircuitBreaker:
    def __init__(self, threshold=5):
        self.threshold = threshold
        self.failures = 0
        self.open = False

    def record_failure(self):
        self.failures += 1
        if self.failures >= self.threshold:
            self.open = True

    def reset(self):
        self.failures = 0
        self.open = False
