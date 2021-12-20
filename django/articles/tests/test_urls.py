from django.test import TestCase

class UrlTests(TestCase):
    def test_for_ci(self):
        self.assertEqual(1+1, 2)