class RetryBudget:
    def __init__(self, max_retries=10):
        self.remaining = max_retries

    def consume(self):
        if self.remaining <= 0:
            return False
        self.remaining -= 1
        return True
