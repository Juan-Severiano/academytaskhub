from django.urls import reverse
from ..base_client import ClientBaseTest


class ClientViewTemplateTest(ClientBaseTest):
    def test_client_admin_view_loads_correct_template(self):
        self.create_discipline()
        self.create_teacher()

        url = reverse('client:admin')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'pages/admin.html')

    def test_client_view_loads_correct_template(self):
        data = {'pk': self.person.id}
        url = reverse('client:client', kwargs=data)
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'pages/client.html')

    def test_client_cards_view_loads_correct_template(self):
        data = {
            'pk': self.person.id
        }
        url = reverse('client:cards', kwargs=data)
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'pages/cards.html')

    def test_client_delete_card_view_loads_correct_template(self):
        card = self.create_card()
        data = {
            'pk_card': card.id,
            'pk_person': self.person.id
        }
        url = reverse('client:delete_card', kwargs=data)
        response = self.client.get(url)
        self.assertTemplateNotUsed(response)

    def test_client_update_card_view_loads_correct_template(self):
        card = self.create_card()
        data = {
            'pk_card': card.id,
            'pk_person': self.person.id
        }
        url = reverse('client:update_card', kwargs=data)
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'pages/update_card.html')
