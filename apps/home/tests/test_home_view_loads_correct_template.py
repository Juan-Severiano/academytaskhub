from django.urls import reverse
from parameterized import parameterized
from django.test import TestCase


class HomeViewTemplateTest(TestCase):
    @parameterized.expand([
        ('home:home', 'pages/home.html'),
        ('home:specific_status', 'pages/specific_status.html'),
        ('home:terms', 'pages/terms.html'),
    ])
    def test_home_views_loads_correct_template(self, url_name, template):
        if 'specific_status' in url_name:
            url = reverse(url_name, kwargs={'status': 'todo'})
        else:
            url = reverse(url_name)
        response = self.client.get(url)
        self.assertTemplateUsed(response, template)
