import pytest
from selenium.webdriver.common.by import By
from django.urls import reverse
from .base_client_functional import ClientBaseTest


@pytest.mark.functional_test
class CLientDeleteCardTest(ClientBaseTest):
    def test_client_delete_card_user_cannot_access_error_message(self):
        self.make_login(level='AL')
        person = self.create_person({
            'username': 'User',
            'email': 'email@gmail.com'
        })
        card = self.create_card(self.person.user)

        data = {'pk_card': card.id, 'pk_person': person.id}
        url = reverse('client:delete_card', kwargs=data)
        self.browser.get(self.live_server_url + url)

        message = self.browser.find_element(By.ID, 'message-alert-id').text
        url_redirect = self.live_server_url + reverse('home:home')

        self.assertEqual(
            'Você não tem permissão de acessar está página.',
            message
        )
        self.assertEqual(url_redirect, self.browser.current_url)

    def test_client_delete_card_person_not_found_404(self):
        self.make_login(level='AL')

        data = {'pk_card': 999, 'pk_person': 999}
        url = reverse('client:delete_card', kwargs=data)
        self.browser.get(self.live_server_url + url)

        message = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Not Found', message)

    def test_client_delete_card_card_not_found_404(self):
        self.make_login(level='AL')

        data = {'pk_card': 999, 'pk_person': self.person.id}
        url = reverse('client:delete_card', kwargs=data)
        self.browser.get(self.live_server_url + url)

        message = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Not Found', message)

    def test_client_delete_card_is_success_message_success(self):
        self.make_login(level='AL')
        card = self.create_card(self.person.user)

        data = {'pk_card': card.id, 'pk_person': self.person.id}
        url = reverse('client:delete_card', kwargs=data)
        self.browser.get(self.live_server_url + url)

        message = self.browser.find_element(By.ID, 'message-alert-id').text
        url_redirect = reverse('client:cards', kwargs={'pk': self.person.id})
        url_redirect = self.live_server_url + url_redirect

        self.assertIn('Card deletado com sucesso.', message)
        self.assertEqual(url_redirect, self.browser.current_url)
