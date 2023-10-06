from django.urls import reverse
from .base_home import HomeBaseTest
from apps.client.models import Person, ItemList
from django.utils import timezone


class HomeViewHomeTest(HomeBaseTest):
    def test_home_view_home_returns_correct_amount_TODO_entity(self):
        self.create_and_login()
        person = Person.objects.get(id=self.person.id)

        for status in ['TODO'] * 3:
            person.item_list.add(self.create_card(
                author=self.user, status=status,
            ))

        url = reverse('home:home')
        response = self.client.get(url)
        context = response.context['item_list_todo'].count()

        person_TODO = person.item_list.filter(status='TODO').count()

        self.assertEqual(context, person_TODO)

    def test_home_view_home_returns_correct_amount_DOING_entity(self):
        self.create_and_login()
        person = Person.objects.get(id=self.person.id)

        for status in ['DOING'] * 3:
            person.item_list.add(self.create_card(
                author=self.user, status=status
            ))

        url = reverse('home:home')
        response = self.client.get(url)
        context = response.context['item_list_doing'].count()

        person_DOING = person.item_list.filter(status='DOING').count()

        self.assertEqual(context, person_DOING)

    def test_home_view_home_returns_correct_amount_DONE_entity(self):
        self.create_and_login()
        person = Person.objects.get(id=self.person.id)

        for status in ['DONE'] * 3:
            person.item_list.add(self.create_card(
                author=self.user, status=status
            ))

        url = reverse('home:home')
        response = self.client.get(url)
        context = response.context['item_list_done'].count()

        person_DONE = person.item_list.filter(status='DONE').count()

        self.assertEqual(context, person_DONE)

    def test_home_view_home_returns_correct_atual_date(self):
        self.create_and_login()
        atual_date = timezone.now().strftime("%Y-%m-%d")

        url = reverse('home:home')
        response = self.client.get(url)
        context = response.context['atual_date']

        self.assertEqual(atual_date, context)

    def test_home_view_home_returns_correct_person(self):
        self.create_and_login()
        person = Person.objects.get(id=self.person.id)

        url = reverse('home:home')
        response = self.client.get(url)
        context = response.context['person']

        self.assertIs(person.id, context.id)

    def test_home_view_home_returns_correct_amount_TODO_entity_logout(self):
        self.user = self.create_user(username='TODO')
        for status in ['TODO'] * 3:
            self.create_card(author=self.user, status=status)

        url = reverse('home:home')
        response = self.client.get(url)
        context = response.context['item_list_todo'].count()

        to_do = ItemList.objects.filter(
            type='A', status='TODO', root=True
        ).count()

        self.assertEqual(context, to_do)

    def test_home_view_home_returns_correct_amount_DOING_entity_logout(self):
        self.user = self.create_user(username='DOING')

        for status in ['DOING'] * 3:
            self.create_card(author=self.user, status=status)

        url = reverse('home:home')
        response = self.client.get(url)
        context = response.context['item_list_doing'].count()

        doing = ItemList.objects.filter(
            type='A', status='DOING', root=True
        ).count()

        self.assertEqual(context, doing)

    def test_home_view_home_returns_correct_amount_DONE_entity_logout(self):
        self.user = self.create_user(username='DONE')

        for status in ['DONE'] * 3:
            self.create_card(author=self.user, status=status)

        url = reverse('home:home')
        response = self.client.get(url)
        context = response.context['item_list_done'].count()

        done = ItemList.objects.filter(
            type='A', status='DONE', root=True
        ).count()

        self.assertEqual(context, done)

    def test_home_view_home_returns_correct_atual_date_logout(self):
        atual_date = timezone.now().strftime("%Y-%m-%d")

        url = reverse('home:home')
        response = self.client.get(url)
        context = response.context['atual_date']

        self.assertEqual(atual_date, context)

    def test_home_view_home_invalid_request_error_message(self):
        url = reverse('home:home')
        response = self.client.put(url, follow=True)
        content = response.content.decode('utf-8')        

        redirect_url = reverse('home:home')
        self.assertIn('Requisição inválida.', content)
        self.assertEqual(redirect_url, response.wsgi_request.path)
