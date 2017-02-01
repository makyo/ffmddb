from unittest import TestCase

from ffmddb import server


class RunTestCase(TestCase):

    def test_pass(self):
        server.run()
        self.assertEqual(1 + 1, 2)
