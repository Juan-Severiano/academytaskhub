from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized


class AuthURLsTest(TestCase):
    @parameterized.expand([
        ('register', '/auth/register/'),
        ('login', '/auth/login/'),
        ('logout', '/auth/logout/'),
    ])
    def test_auth_url_is_correct(self, url_name, path):
        url = reverse(url_name)
        self.assertEqual(url, path)
