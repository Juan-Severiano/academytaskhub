from django.urls import reverse
from ..base_client import ClientBaseTest
from apps.client.models import Discipline, Teacher
from django.utils import timezone


class ClientViewUpdateCardTest(ClientBaseTest):
    def test_client_update_card_view_invalid_request_error_message(self):
        card = self.create_card()
        data = {'pk_card': card.id, 'pk_person': self.person.id}

        url = reverse('client:update_card', kwargs=data)
        response = self.client.put(url, follow=True)
        content = response.content.decode('utf-8')

        self.assertIn('Requisição inválida.', content)
        self.assertEqual(reverse('home:home'), response.wsgi_request.path)

    def test_client_update_card_view_person_not_found_404(self):
        data = {'pk_card': 999, 'pk_person': 999}
        url = reverse('client:update_card', kwargs=data)
        response = self.client.get(url, follow=True)
        content = response.content.decode('utf-8')

        self.assertIn('Not Found', content)

    def test_client_update_card_view_card_not_found_404(self):
        data = {'pk_card': 999, 'pk_person': self.person.id}
        url = reverse('client:update_card', kwargs=data)
        response = self.client.get(url, follow=True)
        content = response.content.decode('utf-8')

        self.assertIn('Not Found', content)

    def test_client_update_card_view_person_cannot_access_message_error(self):
        user = self.create_user(username='Cannot', password='Access')
        person = self.create_person(user, level='AL')
        card = self.create_card()
        data = {'pk_card': card.id, 'pk_person': person.id}

        url = reverse('client:update_card', kwargs=data)
        response = self.client.get(url, follow=True)
        content = response.content.decode('utf-8')

        menssage_reponse = 'Você não tem permissão de acessar está página.'
        self.assertIn(menssage_reponse, content)
        self.assertEqual(reverse('home:home'), response.wsgi_request.path)

    def test_client_cards_view_returns_correct_card_entity(self):
        card = self.create_card()
        data = {'pk_card': card.id, 'pk_person': self.person.id}

        url = reverse('client:update_card', kwargs=data)
        response = self.client.get(url)
        context = response.context['card']

        self.assertIs(card.id, context.id)

    def test_client_cards_view_returns_correct_person_entity(self):
        card = self.create_card()
        data = {'pk_card': card.id, 'pk_person': self.person.id}

        url = reverse('client:update_card', kwargs=data)
        response = self.client.get(url)
        context = response.context['person']

        self.assertIs(self.person.id, context.id)

    def test_client_cards_view_returns_correct_amount_disciplines_entity(self):
        for i in range(0, 3):
            self.create_discipline(name=f'Name: {i}')

        card = self.create_card()
        data = {'pk_card': card.id, 'pk_person': self.person.id}

        url = reverse('client:update_card', kwargs=data)
        response = self.client.get(url)
        context = response.context['disciplines'].count()

        discipline = Discipline.objects.count()

        self.assertEqual(discipline, context)

    def test_client_cards_view_returns_correct_amount_teachers_entity(self):
        for i in range(0, 3):
            self.create_teacher(name=f'Name: {i}')

        card = self.create_card()
        data = {'pk_card': card.id, 'pk_person': self.person.id}

        url = reverse('client:update_card', kwargs=data)
        response = self.client.get(url)
        context = response.context['teachers'].count()

        discipline = Teacher.objects.count()

        self.assertEqual(discipline, context)

    def test_client_cards_view_discipline_not_found_404(self):
        card = self.create_card()
        data = {'pk_card': card.id, 'pk_person': self.person.id}

        url = reverse('client:update_card', kwargs=data)
        response = self.client.post(url, follow=True)
        content = response.content.decode('utf-8')

        message = (
            'Erro interno no sistema: No Discipline matches the given query.'
        )
        url_redirect = reverse('client:update_card', kwargs=data)
        self.assertIn(message, content)
        self.assertEqual(url_redirect, response.wsgi_request.path)

    def test_client_cards_view_teacher_not_found_404(self):
        card = self.create_card()
        arguments = {'pk_card': card.id, 'pk_person': self.person.id}
        data = {'discipline': card.discipline.id}

        url = reverse('client:update_card', kwargs=arguments)
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')

        message = (
            'Erro interno no sistema: No Teacher matches the given query.'
        )
        url_redirect = reverse('client:update_card', kwargs=arguments)
        self.assertIn(message, content)
        self.assertEqual(url_redirect, response.wsgi_request.path)

    def test_client_view_update_card_title_empty_error_message(self):
        card = self.create_card()
        arguments = {'pk_card': card.id, 'pk_person': self.person.id}
        data = {
            'title': ' ',
            'discipline': card.discipline.id,
            'teacher': card.teacher.id
        }

        url = reverse('client:update_card', kwargs=arguments)
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')

        self.assertIn('Prencha o campo de titulo.', content)
        self.assertEqual(url, response.wsgi_request.path)

    def test_client_view_update_card_content_empty_error_message(self):
        card = self.create_card()
        arguments = {'pk_card': card.id, 'pk_person': self.person.id}
        data = {
            'title': 'Title',
            'content': ' ',
            'discipline': card.discipline.id,
            'teacher': card.teacher.id
        }

        url = reverse('client:update_card', kwargs=arguments)
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')

        self.assertIn('Prencha o campo de conteudo.', content)
        self.assertEqual(url, response.wsgi_request.path)

    def test_client_view_update_card_date_empty_error_message(self):
        card = self.create_card()
        arguments = {'pk_card': card.id, 'pk_person': self.person.id}
        data = {
            'title': 'Title',
            'content': 'Content',
            'due-date': ' ',
            'discipline': card.discipline.id,
            'teacher': card.teacher.id
        }

        url = reverse('client:update_card', kwargs=arguments)
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')

        self.assertIn('Prencha o campo de data.', content)
        self.assertEqual(url, response.wsgi_request.path)

    def test_client_view_update_card_status_empty_error_message(self):
        card = self.create_card()
        arguments = {'pk_card': card.id, 'pk_person': self.person.id}
        data = {
            'title': 'Title',
            'content': 'Content',
            'due-date': timezone.now(),
            'discipline': card.discipline.id,
            'teacher': card.teacher.id,
            'status': ' '
        }

        url = reverse('client:update_card', kwargs=arguments)
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')

        self.assertIn('Seleceione o estado da tarefa.', content)
        self.assertEqual(url, response.wsgi_request.path)

    def test_client_view_update_card_is_success_message(self):
        card = self.create_card()
        arguments = {'pk_card': card.id, 'pk_person': self.person.id}
        # date = datetime.strftime(timezone.now(), "%Y-%m-%dT%H:%M")
        data = {
            'title': 'SuccessCard',
            'content': 'SuccessContent',
            'due-date': timezone.now(),
            'discipline': card.discipline.id,
            'teacher': card.teacher.id,
            'status': 'TODO'
        }

        url = reverse('client:update_card', kwargs=arguments)
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')

        url_redirect = reverse('client:cards', kwargs={'pk': self.person.id})
        self.assertIn('Tarefa atualizada com sucesso.', content)
        self.assertEqual(url_redirect, response.wsgi_request.path)
