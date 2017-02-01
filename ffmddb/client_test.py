from unittest import TestCase

from ffmddb import client


class RunTestCase(TestCase):

    def test_pass(self):
        client.run()
        self.assertEqual(1 + 1, 2)
