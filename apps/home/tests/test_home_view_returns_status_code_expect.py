from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized


class ClientViewStatusCodeTest(TestCase):
    @parameterized.expand([
        ('home:home'),
        ('home:specific_status'),
        ('home:terms'),
    ])
    def test_home_views_returns_status_code_200(self, url_name):
        if 'specific_status' in url_name:
            url = reverse(url_name, kwargs={'status': 'todo'})
        else:
            url = reverse(url_name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
