from django.urls import reverse
from .base_client import ClientBaseTest
from apps.client.models import Person, ItemList, Discipline, Teacher
from django.utils import timezone
from datetime import datetime


class ClientViewClientTest(ClientBaseTest):
    def test_client_view_client_not_found_person(self):
        url = reverse('client:client', kwargs={'pk': 2})
        response = self.client.get(url, follow=True)
        content = response.content.decode('utf-8')
        self.assertIn('Not Found', content)

    def test_client_view_client_permission_denied_error_message(self):
        user = self.create_user(username='Denied')
        person = self.create_person(user, level='AL')

        url = reverse('client:client', kwargs={'pk': person.id})
        response = self.client.get(url, follow=True)
        content = response.content.decode('utf-8')

        message = 'Você não tem permissão de acessar está página.'
        self.assertIn(message, content)

    def test_client_view_client_invalid_request_error_message(self):
        url = reverse('client:client', kwargs={'pk': self.person.id})
        response = self.client.put(url, follow=True)
        content = response.content.decode('utf-8')
        self.assertIn('Requisição inválida.', content)

    def test_client_view_client_returns_correct_amount_discipline_entity(self):
        for i in range(0, 3):
            self.create_discipline(name=f'Name: {i}')

        url = reverse('client:client', kwargs={'pk': self.person.id})
        response = self.client.get(url, follow=True)
        context = response.context['disciplines']

        disciplines_size = Discipline.objects.all().count()
        context_size = context.count()
        self.assertEqual(disciplines_size, context_size)

    def test_client_view_client_returns_correct_amount_teacher_entity(self):
        for i in range(0, 3):
            self.create_teacher(name=f'Name: {i}')

        url = reverse('client:client', kwargs={'pk': self.person.id})
        response = self.client.get(url, follow=True)
        context = response.context['teachers']

        teacher_size = Teacher.objects.all().count()
        context_size = context.count()
        self.assertEqual(teacher_size, context_size)

    def test_client_view_client_returns_correct_amount_status_entity(self):
        STATUS = ItemList.STATUS

        url = reverse('client:client', kwargs={'pk': self.person.id})
        response = self.client.get(url, follow=True)
        context = response.context['status']

        status_size = len(STATUS)
        context_size = len(context)
        self.assertEqual(status_size, context_size)

    def test_client_view_client_returns_correct_person_entity(self):
        person = Person.objects.get(id=self.person.id)

        url = reverse('client:client', kwargs={'pk': self.person.id})
        response = self.client.get(url, follow=True)
        context = response.context['person']

        self.assertIs(person.id, context.id)

    def test_client_view_client_title_empty_error_message(self):
        data = {
            'title': ' ',
        }
        url = reverse('client:client', kwargs={'pk': self.person.id})
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('Prencha o campo de titulo.', content)

    def test_client_view_client_content_empty_error_message(self):
        data = {
            'title': 'Title',
            'content': ' '
        }
        url = reverse('client:client', kwargs={'pk': self.person.id})
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('Prencha o campo de conteudo.', content)

    def test_client_view_client_date_empty_error_message(self):
        data = {
            'title': 'Title',
            'content': 'Content',
            'due-date': ' ',
        }
        url = reverse('client:client', kwargs={'pk': self.person.id})
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('Prencha o campo de data.', content)

    def test_client_view_client_discipline_empty_error_message(self):
        data = {
            'title': 'Title',
            'content': 'Content',
            'due-date': timezone.now(),
            'discipline': 1,
        }
        url = reverse('client:client', kwargs={'pk': self.person.id})
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('Selecione uma disciplina.', content)

    def test_client_view_client_teacher_empty_error_message(self):
        discipline = self.create_discipline()
        data = {
            'title': 'Title',
            'content': 'Content',
            'due-date': timezone.now(),
            'discipline': discipline.id,
            'teacher': 1,
        }
        url = reverse('client:client', kwargs={'pk': self.person.id})
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('Selecione um professor.', content)

    def test_client_view_client_status_empty_error_message(self):
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
        url = reverse('client:client', kwargs={'pk': self.person.id})
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('Seleceione o estado da tarefa.', content)

    def test_client_view_client_create_card_is_success_message(self):
        discipline = self.create_discipline()
        teacher = self.create_teacher()

        date = datetime.strftime(timezone.now(), "%Y-%m-%dT%H:%M")

        data = {
            'title': 'SuccessCard',
            'content': 'SuccessContent',
            'due-date': date,
            'discipline': discipline.id,
            'teacher': teacher.id,
            'status': 'TODO'
        }
        url = reverse('client:client', kwargs={'pk': self.person.id})
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('Card criado com sucesso.', content)

    def test_client_view_client_discipline_not_found_404(self):
        data = {'discipline': 999}
        url = reverse('client:client', kwargs={'pk': self.person.id})
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        message = (
            'Erro interno do sistema: &#x27;NoneType&#x27; '
            'object has no attribute &#x27;strip&#x27;'
        )
        self.assertIn(message, content)

    def test_client_view_client_teacher_not_found_404(self):
        discipline = self.create_discipline()
        data = {
            'discipline': discipline.id,
            'teacher': 999,
        }
        url = reverse('client:client', kwargs={'pk': self.person.id})
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        message = (
            'Erro interno do sistema: &#x27;NoneType&#x27; '
            'object has no attribute &#x27;strip&#x27;'
        )
        self.assertIn(message, content)
