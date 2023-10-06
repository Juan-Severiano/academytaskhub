from django.test import TestCase
from django.urls import reverse, resolve
from parameterized import parameterized
from apps.home import views


class HomeFunctionTest(TestCase):
    @parameterized.expand([
        ('home:home', views.home),
        ('home:specific_status', views.specific_status),
        ('home:terms', views.terms),
    ])
    def test_home_view_function_is_correct(self, url_name, correct_view):
        if 'specific_status' in url_name:
            url = reverse('home:specific_status', kwargs={'status': 'todo'})
        else:
            url = reverse(url_name)
        view = resolve(url)
        self.assertIs(view.func, correct_view)
