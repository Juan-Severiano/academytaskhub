from django.urls import reverse
from parameterized import parameterized
from django.test import TestCase


class HomeViewTemplateTest(TestCase):
    @parameterized.expand([
        ('home:home', 'pages/home.html'),
        ('home:to_do', 'pages/to_do.html'),
        ('home:doing', 'pages/doing.html'),
        ('home:done', 'pages/done.html'),
        ('home:terms', 'pages/terms.html'),
    ])
    def test_home_views_loads_correct_template(self, url_name, template):
        url = reverse(url_name)
        response = self.client.get(url)
        self.assertTemplateUsed(response, template)
