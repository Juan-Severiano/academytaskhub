from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized


class HomeURLsTest(TestCase):
    @parameterized.expand([
        ('home:home', '/'),
        ('home:terms', '/terms/'),
    ])
    def test_home_url_is_correct(self, url_name, path):
        url = reverse(url_name)
        self.assertEqual(url, path)

    @parameterized.expand([
        ('todo', '/status/todo/'),
        ('doing', '/status/doing/'),
        ('done', '/status/done/'),
    ])
    def test_home_specific_status_url_is_correct(self, status, path):
        url = reverse('home:specific_status', kwargs={'status': status})
        self.assertEqual(url, path)
