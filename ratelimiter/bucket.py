import time


class TokenBucket:
    """Allows bursts up to `capacity`, refilling at `refill_per_second` tokens per second."""

    def __init__(self, capacity: int, refill_per_second: float, clock=time.monotonic):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if refill_per_second <= 0:
            raise ValueError("refill rate must be positive")
        self.capacity = capacity
        self.rate = refill_per_second
        self._clock = clock
        self._tokens = float(capacity)
        self._last = clock()

    def _refill(self) -> None:
        now = self._clock()
        self._tokens = min(self.capacity, self._tokens + (now - self._last) * self.rate)
        self._last = now

    def allow(self, cost: int = 1) -> bool:
        self._refill()
        if self._tokens >= cost:
            self._tokens -= cost
            return True
        return False

    @property
    def tokens(self) -> float:
        self._refill()
        return self._tokens
