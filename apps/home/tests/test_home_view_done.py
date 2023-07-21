from django.urls import reverse
from .base_home import HomeBaseTest
from apps.client.models import Person, ItemList


class HomeViewDoneTest(HomeBaseTest):
    def test_home_view_done_returns_correct_amount_DONE_entity(self):
        self.create_and_login()
        person = Person.objects.get(id=self.person.id)

        for status in ['DONE'] * 3:
            person.item_list.add(self.create_card(
                author=self.user, status=status
            ))

        url = reverse('home:specific_status', kwargs={'status': 'done'})
        response = self.client.get(url)
        context = response.context['item_list'].count()

        person_DONE = person.item_list.filter(status='DONE').count()

        self.assertEqual(context, person_DONE)

    def test_home_view_done_returns_correct_person(self):
        self.create_and_login()
        person = Person.objects.get(id=self.person.id)

        url = reverse('home:specific_status', kwargs={'status': 'done'})
        response = self.client.get(url)
        context = response.context['person']

        self.assertIs(person.id, context.id)

    def test_home_view_done_returns_correct_amount_DONE_entity_logout(self):
        self.user = self.create_user(username='DONE')

        for status in ['DONE'] * 3:
            self.create_card(author=self.user, status=status)

        url = reverse('home:specific_status', kwargs={'status': 'done'})
        response = self.client.get(url)
        context = response.context['item_list'].count()

        done = ItemList.objects.filter(
            type='A', status='DONE', root=True
        ).count()

        self.assertEqual(context, done)

    def test_home_view_done_invalid_request_error_message(self):
        url = reverse('home:specific_status', kwargs={'status': 'done'})
        response = self.client.put(url, follow=True)
        content = response.content.decode('utf-8')

        redirect_url = reverse('home:home')
        self.assertIn('Requisição inválida.', content)
        self.assertEqual(redirect_url, response.wsgi_request.path)
