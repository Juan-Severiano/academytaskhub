from django.urls import reverse
from .base_home import HomeBaseTest
from apps.client.models import Person, ItemList


class HomeViewDoingTest(HomeBaseTest):
    def test_home_view_doing_returns_correct_amount_DOING_entity(self):
        self.create_and_login()
        person = Person.objects.get(id=self.person.id)

        for status in ['DOING'] * 3:
            person.item_list.add(self.create_card(
                author=self.user, status=status
            ))

        url = reverse('home:doing')
        response = self.client.get(url)
        context = response.context['item_list_doing'].count()

        person_DOING = person.item_list.filter(status='DOING').count()

        self.assertEqual(context, person_DOING)

    def test_home_view_doing_returns_correct_person(self):
        self.create_and_login()
        person = Person.objects.get(id=self.person.id)

        url = reverse('home:doing')
        response = self.client.get(url)
        context = response.context['person']

        self.assertIs(person.id, context.id)

    def test_home_view_doing_returns_correct_amount_DOING_entity_logout(self):
        self.user = self.create_user(username='DOING')

        for status in ['DOING'] * 3:
            self.create_card(author=self.user, status=status)

        url = reverse('home:doing')
        response = self.client.get(url)
        context = response.context['item_list_doing'].count()

        doing = ItemList.objects.filter(
            type='A', status='DOING', root=True
        ).count()

        self.assertEqual(context, doing)

    def test_home_view_doing_invalid_request_error_message(self):
        url = reverse('home:doing')
        response = self.client.put(url, follow=True)
        content = response.content.decode('utf-8')

        redirect_url = reverse('home:home')
        self.assertIn('Requisição inválida.', content)
        self.assertEqual(redirect_url, response.wsgi_request.path)
