from django.urls import reverse
from parameterized import parameterized
from django.test import TestCase


class AuthViewTemplateTest(TestCase):
    @parameterized.expand([
        ('auth:register', 'pages/register.html'),
        ('auth:login', 'pages/login.html'),
    ])
    def test_auth_views_loads_correct_template(self, url_name, template):
        url = reverse(url_name)
        response = self.client.get(url)
        self.assertTemplateUsed(response, template)
