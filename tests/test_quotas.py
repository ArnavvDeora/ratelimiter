from clock import FakeClock
from ratelimiter.quotas import QuotaManager


def test_allow_returns_a_decision():
    quotas = QuotaManager(2, 1, clock=FakeClock())
    assert isinstance(quotas.allow("alice"), bool)


def test_users_have_separate_buckets():
    quotas = QuotaManager(1, 1, clock=FakeClock())
    quotas.allow("alice")
    assert quotas.allow("bob") is True


def test_premium_users_are_allowed():
    quotas = QuotaManager(2, 1, clock=FakeClock())
    assert quotas.allow("carol", premium=True)
