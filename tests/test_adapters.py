from unittest import TestCase

from requests_session_plus.adapters import TimeoutAdapter


class TimeoutAdapterTests(TestCase):
    def test_always_pass(self):
        t = TimeoutAdapter()
        self.assertTrue(True)
