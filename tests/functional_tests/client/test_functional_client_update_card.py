import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
from .base_client_functional import ClientBaseTest
from apps.client.models import Discipline, Teacher


@pytest.mark.functional_test
class CLientUpdateCardTest(ClientBaseTest):
    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/section/main/form'
        )

    def form_field_test_with_callback(self, callback):
        Discipline.objects.create(name='Discipline')
        Teacher.objects.create(name='Teacher')

        self.make_login()
        self.create_card(self.person.user)
        data = {'pk_card': self.card.id, 'pk_person': self.person.id}

        url = reverse('client:update_card', kwargs=data)
        self.browser.get(self.live_server_url + url)

        form = self.get_form()
        callback(form)
        return form

    def test_client_update_card_empty_title_error_message(self):
        def callback(form):
            title = form.find_element(By.NAME, 'title')
            title.clear()
            title.send_keys(' ')
            form.submit()

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            data = {'pk_card': self.card.id, 'pk_person': self.person.id}
            url_redirect = reverse('client:update_card', kwargs=data)
            url_redirect = self.live_server_url + url_redirect

            self.assertIn('Prencha o campo de titulo.', message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)

    def test_client_update_card_empty_content_error_message(self):
        def callback(form):
            content = form.find_element(By.NAME, 'content')
            content.clear()
            content.send_keys(' ')
            form.submit()

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            data = {'pk_card': self.card.id, 'pk_person': self.person.id}
            url_redirect = reverse('client:update_card', kwargs=data)
            url_redirect = self.live_server_url + url_redirect

            self.assertIn('Prencha o campo de conteudo.', message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)

    def test_client_update_card_empty_due_date_error_message(self):
        def callback(form):
            due_date = form.find_element(By.NAME, 'due-date')
            due_date.send_keys((Keys.BACKSPACE + Keys.RIGHT) * 6)
            form.submit()

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            data = {'pk_card': self.card.id, 'pk_person': self.person.id}
            url_redirect = reverse('client:update_card', kwargs=data)
            url_redirect = self.live_server_url + url_redirect

            self.assertIn('Prencha o campo de data.', message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)

    def test_client_update_card_empty_discipline_error_message(self):
        def callback(form):
            self.browser.execute_script(
                "arguments[0].setAttribute('value', 999)",
                form.find_element(
                    By.XPATH,
                    '/html/body/section/main/form/select[1]/option[2]'
                ))
            form.submit()

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            data = {'pk_card': self.card.id, 'pk_person': self.person.id}
            url_redirect = reverse('client:update_card', kwargs=data)
            url_redirect = self.live_server_url + url_redirect

            message_response = (
                'Erro interno no sistema: No Discipline '
                'matches the given query.'
            )
            self.assertIn(message_response, message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)

    def test_client_update_card_empty_teacher_error_message(self):
        def callback(form):
            self.browser.execute_script(
                "arguments[0].setAttribute('value', 999)",
                form.find_element(
                    By.XPATH,
                    '/html/body/section/main/form/select[2]/option[2]'
                ))
            form.submit()

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            data = {'pk_card': self.card.id, 'pk_person': self.person.id}
            url_redirect = reverse('client:update_card', kwargs=data)
            url_redirect = self.live_server_url + url_redirect

            message_response = (
                'Erro interno no sistema: No Teacher '
                'matches the given query.'
            )
            self.assertIn(message_response, message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)

    def test_client_update_card_empty_status_error_message(self):
        def callback(form):
            self.browser.execute_script(
                "arguments[0].setAttribute('value', ' ')",
                form.find_element(
                    By.XPATH,
                    '/html/body/section/main/form/select[3]/option[2]'
                ))
            form.submit()

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            data = {'pk_card': self.card.id, 'pk_person': self.person.id}
            url_redirect = reverse('client:update_card', kwargs=data)
            url_redirect = self.live_server_url + url_redirect

            self.assertIn('Seleceione o estado da tarefa.', message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)

    def test_client_update_card_is_success_message_success(self):
        def callback(form):
            form.find_element(By.NAME, 'title').send_keys('Update')
            form.submit()

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            data = {'pk': self.person.id}
            url_redirect = reverse('client:cards', kwargs=data)
            url_redirect = self.live_server_url + url_redirect

            self.assertIn('Tarefa atualizada com sucesso.', message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)

    def test_client_update_card_user_cannot_access_error_message(self):
        self.make_login(level='AL')
        person = self.create_person({
            'username': 'User',
            'email': 'email@gmail.com'
        })
        card = self.create_card(self.person.user)

        data = {'pk_card': card.id, 'pk_person': person.id}
        url = reverse('client:update_card', kwargs=data)
        self.browser.get(self.live_server_url + url)

        message = self.browser.find_element(By.ID, 'message-alert-id').text
        url_redirect = self.live_server_url + reverse('home:home')

        self.assertEqual(
            'Você não tem permissão de acessar está página.',
            message
        )
        self.assertEqual(url_redirect, self.browser.current_url)

    def test_client_update_card_person_not_found_404(self):
        self.make_login(level='AL')

        data = {'pk_card': 999, 'pk_person': 999}
        url = reverse('client:update_card', kwargs=data)
        self.browser.get(self.live_server_url + url)

        message = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Not Found', message)

    def test_client_update_card_card_not_found_404(self):
        self.make_login(level='AL')

        data = {'pk_card': 999, 'pk_person': self.person.id}
        url = reverse('client:update_card', kwargs=data)
        self.browser.get(self.live_server_url + url)

        message = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Not Found', message)
