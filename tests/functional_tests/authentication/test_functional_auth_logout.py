import pytest
from selenium.webdriver.common.by import By
from django.urls import reverse

from .base_auth_functional import AuthBaseTest


@pytest.mark.functional_test
class AuthLogoutTest(AuthBaseTest):
    def test_auth_logout_invalid_request_error_message(self):
        self.make_login()

        url = reverse('auth:logout')
        self.browser.get(self.live_server_url + url)

        message = self.browser.find_element(By.ID, 'message-alert-id').text
        url_redirect = self.live_server_url + reverse('home:home')

        self.assertEqual('Requisição de logout inválida.', message)
        self.assertEqual(url_redirect, self.browser.current_url)

    def test_auth_logout_is_success_message_success(self):
        self.make_login()

        url = reverse('home:home')
        self.browser.get(self.live_server_url + url)
        self.browser.find_element(
            By.XPATH, '/html/body/header/nav/ul/li[3]/ul/li[8]/form'
        ).submit()

        message = self.browser.find_element(By.ID, 'message-alert-id').text
        url_redirect = self.live_server_url + reverse('auth:login')

        self.assertEqual('Logout realizado com sucesso.', message)
        self.assertEqual(url_redirect, self.browser.current_url)

    def test_auth_logout_invalid_user_error_message(self):
        self.make_login()

        url = reverse('home:home')
        self.browser.get(self.live_server_url + url)
        form = self.browser.find_element(
            By.XPATH, '/html/body/header/nav/ul/li[3]/ul/li[8]/form'
        )

        hidden_element = form.find_element(By.NAME, 'username')
        self.browser.execute_script(
            "arguments[0].setAttribute('value', 'invaliduser')",
            hidden_element
        )
        form.submit()

        message = self.browser.find_element(By.ID, 'message-alert-id').text
        url_redirect = self.live_server_url + reverse('home:home')

        self.assertEqual('User logout inválido.', message)
        self.assertEqual(url_redirect, self.browser.current_url)
