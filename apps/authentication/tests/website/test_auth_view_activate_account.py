import os

from django.urls import reverse
from ..base_auth import AuthBaseTest

from utils.token_generate import vigenere_encrypt


class AuthViewActivateAccountTest(AuthBaseTest):
    def test_auth_activate_account_view_user_already_active(self):
        key = os.environ.get('KEY_TOKEN')
        email = 'useralreadyactive@gmail.com'
        self.create_user(email=email)

        token = vigenere_encrypt(email, key)
        url = reverse('auth:activate_account', args=(token, ))
        url_redirect = reverse('auth:login')

        response = self.client.get(url, follow=True)
        content = response.content.decode('utf-8')

        self.assertIn('Usuário já está ativo.', content)
        self.assertEqual(response.wsgi_request.path, url_redirect)

    def test_auth_activate_account_view_user_active_is_success(self):
        key = os.environ.get('KEY_TOKEN')
        email = 'useralreadyactive@gmail.com'

        user = self.create_user(email=email)
        user.is_active = False
        user.save()

        token = vigenere_encrypt(email, key)
        url = reverse('auth:activate_account', args=(token, ))
        url_redirect = reverse('auth:login')

        response = self.client.get(url, follow=True)
        content = response.content.decode('utf-8')

        self.assertIn('Usuário ativo com sucesso.', content)
        self.assertEqual(response.wsgi_request.path, url_redirect)

    def test_auth_activate_account_view_invalid_code(self):
        key = 'invalid'
        email = 'useralreadyactive@gmail.com'
        self.create_user(email=email)

        token = vigenere_encrypt(email, key)
        url = reverse('auth:activate_account', args=(token, ))
        url_redirect = reverse('home:home')

        response = self.client.get(url, follow=True)
        content = response.content.decode('utf-8')

        self.assertIn('Codigo inválido.', content)
        self.assertEqual(response.wsgi_request.path, url_redirect)
