from django.urls import reverse
from .base_client import ClientBaseTest
from apps.client.models import Person, ItemList, Discipline, Teacher
from apps.client.views import add_card_person
from django.utils import timezone
from datetime import datetime


class ClientViewAdminTest(ClientBaseTest):
    def test_client_view_admin_permission_denied_error_message(self):
        person = Person.objects.get(id=self.person.id)
        person.level = 'AL'
        person.save()

        url = reverse('client:admin')
        response = self.client.get(url, follow=True)
        content = response.content.decode('utf-8')
        message = 'Você não tem permissão de acessar está página.'

        url_redirect = reverse('home:home')
        self.assertIn(message, content)
        self.assertEqual(url_redirect, response.wsgi_request.path)

    def test_client_view_admin_title_empty_error_message(self):
        data = {
            'title': ' ',
        }
        url = reverse('client:admin')
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        url_redirect = reverse('client:admin')

        self.assertIn('Prencha o campo de titulo.', content)
        self.assertEqual(url_redirect, response.wsgi_request.path)

    def test_client_view_admin_content_empty_error_message(self):
        data = {
            'title': 'Title',
            'content': ' '
        }
        url = reverse('client:admin')
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        url_redirect = reverse('client:admin')

        self.assertIn('Prencha o campo de conteudo.', content)
        self.assertEqual(url_redirect, response.wsgi_request.path)

    def test_client_view_admin_date_empty_error_message(self):
        data = {
            'title': 'Title',
            'content': 'Content',
            'due-date': ' ',
        }
        url = reverse('client:admin')
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        url_redirect = reverse('client:admin')

        self.assertIn('Prencha o campo de data.', content)
        self.assertEqual(url_redirect, response.wsgi_request.path)

    def test_client_view_admin_discipline_empty_error_message(self):
        data = {
            'title': 'Title',
            'content': 'Content',
            'due-date': timezone.now(),
            'discipline': 1,
        }
        url = reverse('client:admin')
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        url_redirect = reverse('client:admin')

        self.assertIn('Selecione uma disciplina.', content)
        self.assertEqual(url_redirect, response.wsgi_request.path)

    def test_client_view_admin_teacher_empty_error_message(self):
        discipline = self.create_discipline()
        data = {
            'title': 'Title',
            'content': 'Content',
            'due-date': timezone.now(),
            'discipline': discipline.id,
            'teacher': 1,
        }
        url = reverse('client:admin')
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        url_redirect = reverse('client:admin')

        self.assertIn('Selecione um professor.', content)
        self.assertEqual(url_redirect, response.wsgi_request.path)

    def test_client_view_admin_status_empty_error_message(self):
        discipline = self.create_discipline()
        teacher = self.create_teacher()
        data = {
            'title': 'Title',
            'content': 'Content',
            'due-date': timezone.now(),
            'discipline': discipline.id,
            'teacher': teacher.id,
            'status': ' '
        }
        url = reverse('client:admin')
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        url_redirect = reverse('client:admin')

        self.assertIn('Seleceione o estado da tarefa.', content)
        self.assertEqual(url_redirect, response.wsgi_request.path)

    def test_client_view_admin_create_card_is_success_message(self):
        discipline = self.create_discipline()
        teacher = self.create_teacher()
        due_date_formated = datetime.strftime(timezone.now(), "%Y-%m-%dT%H:%M")
        data = {
            'title': 'SuccessCard',
            'content': 'SuccessContent',
            'due-date': due_date_formated,
            'discipline': discipline.id,
            'teacher': teacher.id,
            'status': 'TODO'
        }
        url = reverse('client:admin')
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        message_success = (
            'Card criado e adicionado a todos os alunos com sucesso.'
        )
        url_redirect = reverse('client:admin')

        self.assertIn(message_success, content)
        self.assertEqual(url_redirect, response.wsgi_request.path)

    def test_client_view_admin_invalid_request_error_message(self):
        url = reverse('client:admin')
        response = self.client.put(url, follow=True)
        content = response.content.decode('utf-8')
        url_redirect = reverse('home:home')

        self.assertIn('Requisição inválida.', content)
        self.assertEqual(url_redirect, response.wsgi_request.path)

    def test_client_view_admin_returns_correct_amount_discipline_entity(self):
        for i in range(0, 3):
            self.create_discipline(name=f'Name: {i}')

        url = reverse('client:admin')
        response = self.client.get(url, follow=True)
        context = response.context['disciplines']

        disciplines_size = Discipline.objects.all().count()
        context_size = context.count()
        self.assertEqual(disciplines_size, context_size)

    def test_client_view_admin_returns_correct_amount_teacher_entity(self):
        for i in range(0, 3):
            self.create_teacher(name=f'Name: {i}')

        url = reverse('client:admin')
        response = self.client.get(url, follow=True)
        context = response.context['teachers']

        teacher_size = Teacher.objects.all().count()
        context_size = context.count()
        self.assertEqual(teacher_size, context_size)

    def test_client_view_admin_returns_correct_amount_status_entity(self):
        STATUS = ItemList.STATUS

        url = reverse('client:admin')
        response = self.client.get(url, follow=True)
        context = response.context['status']

        status_size = len(STATUS)
        context_size = len(context)
        self.assertEqual(status_size, context_size)

    def test_client_view_admin_returns_correct_person_entity(self):
        person = Person.objects.get(id=self.person.id)

        url = reverse('client:admin')
        response = self.client.get(url, follow=True)
        context = response.context['person']

        self.assertIs(person.id, context.id)

    def test_client_add_card_person_returns_number_cards_correctly(self):
        for i in range(0, 4):
            user = self.create_user(username=f'User: {i}')
            self.create_person(user, level='AL')

        discipline = self.create_discipline()
        teacher = self.create_teacher()
        due_date_formated = datetime.strftime(timezone.now(), "%Y-%m-%dT%H:%M")
        data = {
            'author': self.user,
            'title': 'SuccessCard',
            'content': 'SuccessContent',
            'due_date': due_date_formated,
            'discipline': discipline,
            'teacher': teacher,
            'status': 'TODO'
        }
        add_card_person(**data)

        people = Person.objects.filter(level='AL')
        people = people.union(Person.objects.filter(level='AD'))
        people_size = people.count()

        cards_size = ItemList.objects.filter(
            title='SuccessCard', type='A', status='TODO'
        ).count()
        self.assertEqual(people_size, cards_size)

    def test_client_view_admin_discipline_not_found_404(self):
        data = {'discipline': 999}
        url = reverse('client:admin')
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        message = (
            'Erro interno do sistema: &#x27;NoneType&#x27; '
            'object has no attribute &#x27;strip&#x27;'
        )
        url_redirect = reverse('client:admin')

        self.assertIn(message, content)
        self.assertEqual(url_redirect, response.wsgi_request.path)

    def test_client_view_admin_teacher_not_found_404(self):
        discipline = self.create_discipline()
        data = {
            'discipline': discipline.id,
            'teacher': 999,
        }
        url = reverse('client:admin')
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        message = (
            'Erro interno do sistema: &#x27;NoneType&#x27; '
            'object has no attribute &#x27;strip&#x27;'
        )
        url_redirect = reverse('client:admin')

        self.assertIn(message, content)
        self.assertEqual(url_redirect, response.wsgi_request.path)
