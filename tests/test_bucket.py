import pytest

from clock import FakeClock
from ratelimiter import TokenBucket


def test_allows_a_burst_up_to_capacity_then_refuses():
    bucket = TokenBucket(3, 1, FakeClock())
    assert [bucket.allow() for _ in range(4)] == [True, True, True, False]


def test_refills_over_time():
    clock = FakeClock()
    bucket = TokenBucket(2, 0.5, clock)
    bucket.allow(); bucket.allow()
    clock.advance(2)
    assert bucket.allow() is True
    assert bucket.allow() is False


def test_never_exceeds_capacity():
    clock = FakeClock()
    bucket = TokenBucket(2, 10, clock)
    clock.advance(60)
    assert bucket.tokens == 2


def test_cost_greater_than_tokens_is_refused_and_not_charged():
    bucket = TokenBucket(5, 1, FakeClock())
    assert bucket.allow(cost=6) is False
    assert bucket.tokens == 5


@pytest.mark.parametrize("cap, rate", [(0, 1), (1, 0), (-1, 1)])
def test_rejects_bad_config(cap, rate):
    with pytest.raises(ValueError):
        TokenBucket(cap, rate)
