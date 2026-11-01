from clock import FakeClock
from ratelimiter import SlidingWindowLog


def test_limit_within_window():
    clock = FakeClock()
    window = SlidingWindowLog(2, 10, clock)
    assert [window.allow(), window.allow(), window.allow()] == [True, True, False]


def test_old_hits_expire_exactly_at_window_end():
    clock = FakeClock()
    window = SlidingWindowLog(1, 10, clock)
    window.allow()
    clock.advance(9.9)
    assert window.allow() is False
    clock.advance(0.1)
    assert window.allow() is True
