import time
from collections import deque


class SlidingWindowLog:
    """At most `limit` requests in any rolling `window_seconds`."""

    def __init__(self, limit: int, window_seconds: float, clock=time.monotonic):
        if limit <= 0 or window_seconds <= 0:
            raise ValueError("limit and window must be positive")
        self.limit = limit
        self.window = window_seconds
        self._clock = clock
        self._hits = deque()

    def allow(self) -> bool:
        now = self._clock()
        while self._hits and now - self._hits[0] >= self.window:
            self._hits.popleft()
        if len(self._hits) < self.limit:
            self._hits.append(now)
            return True
        return False
