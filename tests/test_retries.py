from unittest import TestCase

from requests_session_plus.retries import SessionPlusRetry


class SessionPlusRetryTests(TestCase):
    def test_always_pass(self):
        s = SessionPlusRetry()
        self.assertTrue(True)
