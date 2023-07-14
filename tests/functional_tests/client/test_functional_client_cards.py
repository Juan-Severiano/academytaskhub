import pytest
from selenium.webdriver.common.by import By
from django.urls import reverse
from .base_client_functional import ClientBaseTest


@pytest.mark.functional_test
class CLientCardsTest(ClientBaseTest):
    def test_client_cards_user_cannot_access_error_message(self):
        self.make_login(level='AL')
        person = self.create_person({
            'username': 'User',
            'email': 'email@gmail.com'
        })
        url = reverse('client:cards', kwargs={'pk': person.id})
        self.browser.get(self.live_server_url + url)

        message = self.browser.find_element(By.ID, 'message-alert-id').text
        url_redirect = self.live_server_url + reverse('home:home')

        self.assertEqual(
            'Você não tem permissão de acessar está página.',
            message
        )
        self.assertEqual(url_redirect, self.browser.current_url)

    def test_client_cards_person_not_found_404(self):
        self.make_login(level='AL')
        url = reverse('client:cards', kwargs={'pk': 999})
        self.browser.get(self.live_server_url + url)

        message = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Not Found', message)
