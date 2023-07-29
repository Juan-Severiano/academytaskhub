from django.test import TestCase
from django.urls import reverse, resolve
from parameterized import parameterized
from apps.authentication import views


class AuthFunctionTest(TestCase):
    @parameterized.expand([
        ('auth:register', views.register),
        ('auth:login', views.login),
        ('auth:logout', views.logout),
    ])
    def test_auth_view_function_is_correct(self, url_name, correct_view):
        url = reverse(url_name)
        view = resolve(url)
        self.assertIs(view.func, correct_view)
