from django.urls import reverse
from .base_auth import AuthBaseTest


class AuthViewLogoutTest(AuthBaseTest):
    def test_auth_logout_view_invalid_request_message_error(self):
        self.login_user_person()
        url = reverse('auth:logout')
        response = self.client.get(url, follow=True)
        content = response.content.decode('utf-8')
        self.assertIn('Requisição de logout inválida.', content)

    def test_auth_logout_view_invalid_user_message_error(self):
        self.login_user_person()
        url = reverse('auth:logout')
        data = {'username': 'invaliduser'}
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('User logout inválido.', content)

    def test_auth_logout_view_message_success(self):
        self.login_user_person()
        url = reverse('auth:logout')
        data = {'username': self.user.username}
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('Logout realizado com sucesso.', content)
