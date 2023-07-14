from django.urls import reverse
from .base_home import HomeBaseTest
from apps.client.models import Person, ItemList


class HomeViewTodoTest(HomeBaseTest):
    def test_home_view_todo_returns_correct_amount_TODO_entity(self):
        self.create_and_login()
        person = Person.objects.get(id=self.person.id)

        for status in ['TODO'] * 3:
            person.item_list.add(self.create_card(
                author=self.user, status=status,
            ))

        url = reverse('home:to_do')
        response = self.client.get(url)
        context = response.context['item_list_todo'].count()

        person_TODO = person.item_list.filter(status='TODO').count()

        self.assertEqual(context, person_TODO)

    def test_home_view_todo_returns_correct_person(self):
        self.create_and_login()
        person = Person.objects.get(id=self.person.id)

        url = reverse('home:to_do')
        response = self.client.get(url)
        context = response.context['person']

        self.assertIs(person.id, context.id)

    def test_home_view_todo_returns_correct_amount_TODO_entity_logout(self):
        self.user = self.create_user(username='TODO')
        for status in ['TODO'] * 3:
            self.create_card(author=self.user, status=status)

        url = reverse('home:to_do')
        response = self.client.get(url)
        context = response.context['item_list_todo'].count()

        to_do = ItemList.objects.filter(
            type='A', status='TODO', root=True
        ).count()

        self.assertEqual(context, to_do)

    def test_home_view_home_invalid_request_error_message(self):
        url = reverse('home:to_do')
        response = self.client.put(url, follow=True)
        content = response.content.decode('utf-8')

        redirect_url = reverse('home:home')
        self.assertIn('Requisição inválida.', content)
        self.assertEqual(redirect_url, response.wsgi_request.path)
