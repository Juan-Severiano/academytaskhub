from django.urls import reverse
from ..base_client import ClientBaseTest
from apps.client.models import Person


class ClientViewCardsTest(ClientBaseTest):
    def test_client_cards_view_person_not_found_404(self):
        url = reverse('client:cards', kwargs={'pk': 999})
        response = self.client.get(url, follow=True)
        content = response.content.decode('utf-8')
        self.assertIn('Not Found', content)

    def test_client_cards_view_cannot_access_message_error(self):
        user = self.create_user(username='Cannot', password='Access')
        person = self.create_person(user, level='AL')

        url = reverse('client:cards', kwargs={'pk': person.id})
        response = self.client.get(url, follow=True)
        content = response.content.decode('utf-8')
        self.assertIn(
            'Você não tem permissão de acessar está página.', content
        )
        self.assertEqual(reverse('home:home'), response.wsgi_request.path)

    def test_client_cards_view_returns_correct_amount_TODO_entity(self):
        person = Person.objects.get(id=self.person.id)

        for status in ['TODO'] * 3:
            person.item_list.add(self.create_card(
                author=self.user, status=status
            ))

        url = reverse('client:cards', kwargs={'pk': self.person.id})
        response = self.client.get(url)
        context = response.context['item_list_todo'].count()

        person_TODO = person.item_list.filter(status='TODO').count()

        self.assertEqual(context, person_TODO)

    def test_client_cards_view_returns_correct_amount_DOING_entity(self):
        person = Person.objects.get(id=self.person.id)

        for status in ['DOING'] * 3:
            person.item_list.add(self.create_card(
                author=self.user, status=status
            ))

        url = reverse('client:cards', kwargs={'pk': self.person.id})
        response = self.client.get(url)
        context = response.context['item_list_doing'].count()

        person_DOING = person.item_list.filter(status='DOING').count()

        self.assertEqual(context, person_DOING)

    def test_client_cards_view_returns_correct_amount_DONE_entity(self):
        person = Person.objects.get(id=self.person.id)

        for status in ['DONE'] * 3:
            person.item_list.add(self.create_card(
                author=self.user, status=status
            ))

        url = reverse('client:cards', kwargs={'pk': self.person.id})
        response = self.client.get(url)
        context = response.context['item_list_done'].count()

        person_DONE = person.item_list.filter(status='DONE').count()

        self.assertEqual(context, person_DONE)

    def test_client_cards_view_returns_correct_person_entity(self):
        person = Person.objects.get(id=self.person.id)

        url = reverse('client:cards', kwargs={'pk': self.person.id})
        response = self.client.get(url)
        context = response.context['person']

        self.assertIs(person.id, context.id)

    def test_client_cards_view_invalid_request_error_message(self):
        url = reverse('client:cards', kwargs={'pk': self.person.id})
        response = self.client.put(url, follow=True)
        content = response.content.decode('utf-8')

        self.assertIn('Requisição inválida.', content)
        self.assertEqual(reverse('home:home'), response.wsgi_request.path)
