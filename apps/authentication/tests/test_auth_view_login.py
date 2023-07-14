from django.urls import reverse
from .base_auth import AuthBaseTest


class AuthViewLoginTest(AuthBaseTest):
    def test_auth_login_view_cannot_access_message_error(self):
        self.login_user_person()
        url = reverse('auth:login')
        response = self.client.get(url, follow=True)
        content = response.content.decode('utf-8')
        self.assertIn('Não pode acessar está pagina estando logado.', content)

    def test_auth_login_view_invalid_request_message_error(self):
        url = reverse('auth:login')
        response = self.client.put(url, follow=True)
        content = response.content.decode('utf-8')
        self.assertIn('Requisição inválida.', content)

    def test_auth_login_view_email_empty_message_error(self):
        url = reverse('auth:login')
        data = {
            'email': '',
        }
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('Prencha o campo de email.', content)

    def test_auth_login_view_email_not_match_message_error(self):
        url = reverse('auth:login')
        data = {
            'email': 'emailinvalid@gmail.com',
        }
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('O email precisa ser do gov.br.', content)

    def test_auth_login_view_password_empty_message_error(self):
        url = reverse('auth:login')
        data = {
            'email': 'existemail@aluno.ce.gov.br',
            'password': ' ',
        }
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('Prencha o campo de senha.', content)

    def test_auth_login_view_lgoin_is_success_message_success(self):
        email = 'login@aluno.ce.gov.br'
        password = 'Pass'
        user = self.create_user(
            password=password,
            email=email
        )
        self.create_person(user, level='AL')
        url = reverse('auth:login')
        data = {
            'email': email,
            'password': password
        }
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('Usuário logou com sucesso.', content)

    def test_auth_login_view_lgoin_is_fail_message_fail(self):
        email = 'login@aluno.ce.gov.br'
        password = 'Pass'
        user = self.create_user(
            password=password,
            email=email
        )
        self.create_person(user, level='AL')
        url = reverse('auth:login')
        data = {
            'email': 'invalid@aluno.ce.gov.br',
            'password': password
        }
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('Não foi possível logar. Tente novamente.', content)
