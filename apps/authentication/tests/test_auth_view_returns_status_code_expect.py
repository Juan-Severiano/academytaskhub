from django.urls import reverse
from parameterized import parameterized
from .base_auth import AuthBaseTest


class AuthViewStatusCodeTest(AuthBaseTest):
    @parameterized.expand([
        ('register', 200, False),
        ('login', 200, False),
        ('logout', 302, True),
    ])
    def test_auth_view_returns_status_code_expect(
        self, url_name, status_code, login_required
    ):
        if login_required:
            self.login_user()
        url = reverse(url_name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)
