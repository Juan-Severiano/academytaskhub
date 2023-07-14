from django.urls import reverse
from .base_client import ClientBaseTest


class ClientViewStatusCodeTest(ClientBaseTest):
    def test_client_admin_view_returns_status_code_200(self):
        self.create_discipline()
        self.create_teacher()

        url = reverse('client:admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_client_view_returns_status_code_200(self):
        data = {
            'pk': self.person.id
        }
        url = reverse('client:client', kwargs=data)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_client_cards_view_returns_status_code_200(self):
        data = {
            'pk': self.person.id
        }
        url = reverse('client:cards', kwargs=data)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_client_delete_card_view_returns_status_code_302(self):
        card = self.create_card()
        data = {
            'pk_card': card.id,
            'pk_person': self.person.id
        }
        url = reverse('client:delete_card', kwargs=data)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_client_update_card_view_returns_status_code_302(self):
        card = self.create_card()
        data = {
            'pk_card': card.id,
            'pk_person': self.person.id
        }
        url = reverse('client:update_card', kwargs=data)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
