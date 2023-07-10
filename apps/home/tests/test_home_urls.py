from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized


class HomeURLsTest(TestCase):
    @parameterized.expand([
        ('home', '/'),
        ('to_do', '/to_do/'),
        ('doing', '/doing/'),
        ('done', '/done/'),
    ])
    def test_home_url_is_correct(self, url_name, path):
        url = reverse(url_name)
        self.assertEqual(url, path)
