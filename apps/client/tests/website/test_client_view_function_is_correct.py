from django.test import TestCase
from django.urls import reverse, resolve
from parameterized import parameterized
from apps.client import views


class ClientFunctionTest(TestCase):
    @parameterized.expand([
        ('client:client', views.client, {'pk': 1}),
        ('client:admin', views.admin, {}),
        ('client:cards', views.cards, {'pk': 1}),
        (
            'client:delete_card', views.delete_card,
            {'pk_card': 1, 'pk_person': 1}
        ),
        (
            'client:update_card', views.update_card,
            {'pk_card': 1, 'pk_person': 1}
        ),
    ])
    def test_client_view_function_is_correct(
        self, url_name, correct_view, data
    ):
        url = reverse(url_name, kwargs=data)
        view = resolve(url)
        self.assertIs(view.func, correct_view)