from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized


class HomeURLsTest(TestCase):
    @parameterized.expand([
        ('home:home', '/'),
        ('home:to_do', '/to_do/'),
        ('home:doing', '/doing/'),
        ('home:done', '/done/'),
        ('home:terms', '/terms/'),
    ])
    def test_home_url_is_correct(self, url_name, path):
        url = reverse(url_name)
        self.assertEqual(url, path)
