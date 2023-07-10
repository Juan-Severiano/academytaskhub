from django.urls import reverse
from parameterized import parameterized
from .base_client import AuthBaseTest


class ClientViewStatusCodeTest(AuthBaseTest):
    @parameterized.expand([
        ('client', 200, {'pk': 1}),
        ('admin', 200, {}),
        ('cards', 200, {'pk': 1}),
        (
            'delete_card', 302,
            {'pk_card': 1, 'pk_person': 1}
        ),
        (
            'update_card', 200,
            {'pk_card': 1, 'pk_person': 1}
        ),
    ])
    def test_client_view_returns_status_code_expect(
        self, url_name, status_code, data
    ):
        self.login_user()
        url = reverse(url_name, kwargs=data)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)
