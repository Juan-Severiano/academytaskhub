import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse

from .base_auth_functional import AuthBaseTest


@pytest.mark.functional_test
class AuthRegisterTest(AuthBaseTest):
    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/section/main/form'
        )

    def form_field_test_with_callback(self, callback):
        url = reverse('auth:register')
        self.browser.get(self.live_server_url + url)

        form = self.get_form()

        form.find_element(By.NAME, 'username').send_keys('Test')
        form.find_element(By.NAME, 'email').send_keys('test@aluno.ce.gov.br')
        form.find_element(By.NAME, 'password').send_keys('Test123')
        form.find_element(By.NAME, 'confirm-password').send_keys('Test123')

        callback(form)
        return form

    def test_auth_register_cannot_access_error_message(self):
        self.make_login()
        url = reverse('auth:register')
        self.browser.get(self.live_server_url + url)

        message = self.browser.find_element(By.ID, 'message-alert-id').text
        url_redirect = self.live_server_url + reverse('home:home')

        self.assertEqual(
            'Não pode acessar está pagina estando logado.',
            message
        )
        self.assertEqual(url_redirect, self.browser.current_url)

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = form.find_element(By.NAME, 'username')
            username_field.clear()
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            url_redirect = self.live_server_url + reverse('auth:register')

            self.assertIn('Prencha o campo de username.', message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)

    def test_empty_email_error_message(self):
        def callback(form):
            username_field = form.find_element(By.NAME, 'email')
            username_field.clear()
            username_field.send_keys(' ')
            form.submit()

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            url_redirect = self.live_server_url + reverse('auth:register')

            self.assertIn('Prencha o campo de email.', message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)

    def test_email_is_not_gov_error_message(self):
        def callback(form):
            username_field = form.find_element(By.NAME, 'email')
            username_field.clear()
            username_field.send_keys('invalid@gmail.com')
            username_field.send_keys(Keys.ENTER)

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            url_redirect = self.live_server_url + reverse('auth:register')

            self.assertIn('O email precisa ser do gov.br.', message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)

    def test_email_already_used_error_message(self):
        self.create_user()

        def callback(form):
            username_field = form.find_element(By.NAME, 'email')
            username_field.clear()
            username_field.send_keys('test@aluno.ce.gov.br')
            username_field.send_keys(Keys.ENTER)

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            url_redirect = self.live_server_url + reverse('auth:register')

            self.assertIn('Email já utilizado.', message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)

    def test_empty_password_error_message(self):
        def callback(form):
            username_field = form.find_element(By.NAME, 'password')
            username_field.clear()
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            url_redirect = self.live_server_url + reverse('auth:register')

            self.assertIn('Prencha o campo de senha.', message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)

    def test_empty_confirm_password_error_message(self):
        def callback(form):
            username_field = form.find_element(By.NAME, 'confirm-password')
            username_field.clear()
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            url_redirect = self.live_server_url + reverse('auth:register')

            self.assertIn('Prencha o campo de confirmar senha.', message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)

    def test_passwords_does_not_match_error_message(self):
        def callback(form):
            username_field = form.find_element(By.NAME, 'password')
            username_field.clear()
            username_field.send_keys('invalid')
            username_field.send_keys(Keys.ENTER)

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            url_redirect = self.live_server_url + reverse('auth:register')

            self.assertIn('As senhas não coicidem.', message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)

    def test_auth_register_is_success_message_success(self):
        def callback(form):
            form.submit()

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            url_redirect = self.live_server_url + reverse('auth:login')

            self.assertEqual('Registro realizado com sucesso.', message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)
