import time

from .bucket import TokenBucket


class QuotaManager:
    def __init__(self, capacity: int, refill_per_second: float, premium_multiplier: int = 2,
                 clock=time.monotonic):
        self.capacity = capacity
        self.refill = refill_per_second
        self.premium_multiplier = premium_multiplier
        self._clock = clock
        self._buckets = {}

    def _bucket(self, user_id: str, premium: bool) -> TokenBucket:
        if user_id not in self._buckets:
            capacity = self.capacity * self.premium_multiplier if premium else self.capacity
            self._buckets[user_id] = TokenBucket(capacity, self.refill, self._clock)
        return self._buckets[user_id]

    def allow(self, user_id: str, premium: bool = False) -> bool:
        return self._bucket(user_id, premium).allow()
