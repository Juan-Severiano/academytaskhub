from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized


class ClientViewStatusCodeTest(TestCase):
    @parameterized.expand([
        ('home:home'),
        ('home:to_do'),
        ('home:doing'),
        ('home:done'),
        ('home:terms'),
    ])
    def test_home_views_returns_status_code_200(self, url_name):
        url = reverse(url_name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
