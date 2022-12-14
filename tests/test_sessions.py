from unittest import TestCase

from requests_session_plus.sessions import SessionPlus


class SessionPlusTests(TestCase):
    def test_always_pass(self):
        s = SessionPlus()
        self.assertTrue(True)
