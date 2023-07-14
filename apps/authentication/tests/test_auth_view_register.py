from django.urls import reverse
from .base_auth import AuthBaseTest
from apps.authentication.views import copy_card
from apps.client.models import Person, ItemList


class AuthViewRegisterTest(AuthBaseTest):
    def test_auth_register_view_cannot_access_message_error(self):
        self.login_user_person()
        url = reverse('auth:register')
        response = self.client.get(url, follow=True)
        content = response.content.decode('utf-8')
        self.assertIn('Não pode acessar está pagina estando logado.', content)

    def test_auth_register_view_invalid_request_message_error(self):
        url = reverse('auth:register')
        response = self.client.put(url, follow=True)
        content = response.content.decode('utf-8')
        self.assertIn('Requisição inválida.', content)

    def test_auth_register_view_username_empty_message_error(self):
        url = reverse('auth:register')
        data = {'username': ' '}
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('Prencha o campo de username.', content)

    def test_auth_register_view_email_empty_message_error(self):
        url = reverse('auth:register')
        data = {
            'username': 'User',
            'email': '',
        }
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('Prencha o campo de email.', content)

    def test_auth_register_view_email_not_match_message_error(self):
        url = reverse('auth:register')
        data = {
            'username': 'User',
            'email': 'emailinvalid@gmail.com',
        }
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('O email precisa ser do gov.br.', content)

    def test_auth_register_view_email_exist_message_error(self):
        self.create_user(email='existemail@aluno.ce.gov.br')
        url = reverse('auth:register')
        data = {
            'username': 'User',
            'email': 'existemail@aluno.ce.gov.br',
        }
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('Email já utilizado.', content)

    def test_auth_register_view_password_empty_message_error(self):
        url = reverse('auth:register')
        data = {
            'username': 'User',
            'email': 'existemail@aluno.ce.gov.br',
            'password': ' ',
        }
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('Prencha o campo de senha.', content)

    def test_auth_register_view_confirm_password_empty_message_error(self):
        url = reverse('auth:register')
        data = {
            'username': 'User',
            'email': 'existemail@aluno.ce.gov.br',
            'password': 'Pass',
            'confirm-password': ' '
        }
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('Prencha o campo de confirmar senha.', content)

    def test_auth_register_view_passwords_not_match_message_error(self):
        url = reverse('auth:register')
        data = {
            'username': 'User',
            'email': 'existemail@aluno.ce.gov.br',
            'password': 'Pass',
            'confirm-password': 'invalid'
        }
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('As senhas não coicidem.', content)

    def test_auth_register_view_register_is_succes(self):
        url = reverse('auth:register')
        data = {
            'username': 'User',
            'email': 'existemail@aluno.ce.gov.br',
            'password': 'Pass',
            'confirm-password': 'Pass'
        }
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        self.assertIn('Registro realizado com sucesso.', content)

    def test_auth_register_view_register_except(self):
        self.create_user()
        url = reverse('auth:register')
        data = {
            'username': 'User',
            'email': 'existemail@aluno.ce.gov.br',
            'password': 'Pass',
            'confirm-password': 'Pass'
        }
        response = self.client.post(url, follow=True, data=data)
        content = response.content.decode('utf-8')
        message = (
            'Erro interno no sistema: UNIQUE '
            'constraint failed: auth_user.username'
        )
        self.assertIn(message, content)

    def test_auth_copy_card_return_correct(self):
        card = self.create_card()
        card_copy = copy_card(card)

        self.assertEqual(card.author, card_copy.author)
        self.assertEqual(card.title, card_copy.title)
        self.assertEqual(card.content, card_copy.content)
        self.assertEqual(card.due_date, card_copy.due_date)
        self.assertEqual(card.discipline, card_copy.discipline)
        self.assertEqual(card.teacher, card_copy.teacher)
        self.assertEqual(card.status, card_copy.status)
        self.assertEqual(card.type, card_copy.type)

    def test_auth_register_fors_returns_correct_entity(self):
        for status in ['TODO', 'DOING', 'DONE']:
            self.create_card(
                status=status, type='A', root=True,
                author={'username': status, 'email': f'{status}@gmail.com'}
            )

        url = reverse('auth:register')
        data = {
            'username': 'User',
            'email': 'existemail@aluno.ce.gov.br',
            'password': 'Pass',
            'confirm-password': 'Pass'
        }
        self.client.post(url, follow=True, data=data)

        to_do = len(list(ItemList.objects.filter(
            status='TODO', type='A', root=True)))
        doing = len(list(ItemList.objects.filter(
            status='DOING', type='A', root=True)))
        done = len(list(ItemList.objects.filter(
            status='DONE', type='A', root=True)))

        person = Person.objects.first()
        person_to_do = len(list(person.item_list.filter(
            status='TODO', type='A')))
        person_doing = len(list(person.item_list.filter(
            status='DOING', type='A')))
        person_done = len(list(person.item_list.filter(
            status='DONE', type='A')))

        self.assertEqual(to_do, person_to_do)
        self.assertEqual(doing, person_doing)
        self.assertEqual(done, person_done)

    def test_auth_register_fors_returns_empty_entity(self):
        url = reverse('auth:register')
        data = {
            'username': 'User',
            'email': 'existemail@aluno.ce.gov.br',
            'password': 'Pass',
            'confirm-password': 'Pass'
        }
        self.client.post(url, follow=True, data=data)

        to_do = len(list(ItemList.objects.filter(
            status='TODO', type='A', root=True)))
        doing = len(list(ItemList.objects.filter(
            status='DOING', type='A', root=True)))
        done = len(list(ItemList.objects.filter(
            status='DONE', type='A', root=True)))

        person = Person.objects.first()
        person_to_do = len(list(person.item_list.filter(
            status='TODO', type='A')))
        person_doing = len(list(person.item_list.filter(
            status='DOING', type='A')))
        person_done = len(list(person.item_list.filter(
            status='DONE', type='A')))

        self.assertEqual(to_do, person_to_do)
        self.assertEqual(doing, person_doing)
        self.assertEqual(done, person_done)
