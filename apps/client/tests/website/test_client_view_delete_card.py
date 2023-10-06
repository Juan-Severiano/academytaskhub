from django.urls import reverse
from ..base_client import ClientBaseTest


class ClientViewDeleteCardTest(ClientBaseTest):
    def test_client_delete_card_view_invalid_request_error_message(self):
        data = {'pk_card': 999, 'pk_person': 999}
        url = reverse('client:delete_card', kwargs=data)
        response = self.client.put(url, follow=True)
        content = response.content.decode('utf-8')

        self.assertIn('Requisição inválida.', content)
        self.assertEqual(reverse('home:home'), response.wsgi_request.path)

    def test_client_delete_card_view_person_not_found_404(self):
        data = {'pk_card': 999, 'pk_person': 999}
        url = reverse('client:delete_card', kwargs=data)
        response = self.client.get(url, follow=True)
        content = response.content.decode('utf-8')

        self.assertIn('Not Found', content)

    def test_client_delete_card_view_card_not_found_404(self):
        data = {'pk_card': 999, 'pk_person': self.person.id}
        url = reverse('client:delete_card', kwargs=data)
        response = self.client.get(url, follow=True)
        content = response.content.decode('utf-8')

        self.assertIn('Not Found', content)

    def test_client_delete_card_view_person_cannot_access_message_error(self):
        user = self.create_user(username='Cannot', password='Access')
        person = self.create_person(user, level='AL')
        data = {'pk_card': 999, 'pk_person': person.id}

        url = reverse('client:delete_card', kwargs=data)
        response = self.client.get(url, follow=True)
        content = response.content.decode('utf-8')

        message_response = 'Você não tem permissão de acessar está página.'
        self.assertIn(message_response, content)
        self.assertEqual(reverse('home:home'), response.wsgi_request.path)

    def test_client_delete_card_view_delete_is_success_message_success(self):
        card = self.create_card()
        data = {'pk_card': card.id, 'pk_person': self.person.id}

        url = reverse('client:delete_card', kwargs=data)
        response = self.client.get(url, follow=True)
        content = response.content.decode('utf-8')

        self.assertIn('Card deletado com sucesso.', content)

        url_redirect = reverse('client:cards', kwargs={'pk': self.person.id})
        self.assertEqual(url_redirect, response.wsgi_request.path)
