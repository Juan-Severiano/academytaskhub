from django.test import TestCase
from django.urls import reverse, resolve
from parameterized import parameterized
from apps.home import views


class HomeFunctionTest(TestCase):
    @parameterized.expand([
        ('home', views.home),
        ('to_do', views.to_do),
        ('doing', views.doing),
        ('done', views.done),
    ])
    def test_client_view_function_is_correct(self, url_name, correct_view):
        url = reverse(url_name)
        view = resolve(url)
        self.assertIs(view.func, correct_view)
