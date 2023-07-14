from django.test import TestCase
from django.urls import reverse, resolve
from parameterized import parameterized
from apps.home import views


class HomeFunctionTest(TestCase):
    @parameterized.expand([
        ('home:home', views.home),
        ('home:to_do', views.to_do),
        ('home:doing', views.doing),
        ('home:done', views.done),
        ('home:terms', views.terms),
    ])
    def test_client_view_function_is_correct(self, url_name, correct_view):
        url = reverse(url_name)
        view = resolve(url)
        self.assertIs(view.func, correct_view)
