import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
from .base_client_functional import ClientBaseTest
from apps.client.models import Discipline, Teacher


@pytest.mark.functional_test
class CLientClientTest(ClientBaseTest):
    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/section/main/form'
        )

    def form_field_test_with_callback(self, callback):
        Discipline.objects.create(name='Discipline')
        Teacher.objects.create(name='Teacher')

        self.make_login()
        url = reverse('client:client', kwargs={'pk': self.person.id})
        self.browser.get(self.live_server_url + url)

        form = self.get_form()

        form.find_element(By.NAME, 'title').send_keys('Title Test')
        form.find_element(By.NAME, 'content').send_keys('Content Test')

        form.find_element(By.NAME, 'due_date').send_keys(
            (Keys.UP + Keys.RIGHT) * 6
        )

        callback(form)
        return form

    def test_client_client_user_cannot_access_error_message(self):
        self.make_login(level='AL')
        person = self.create_person({
            'username': 'User',
            'email': 'email@gmail.com'
        })
        url = reverse('client:client', kwargs={'pk': person.id})
        self.browser.get(self.live_server_url + url)

        message = self.browser.find_element(By.ID, 'message-alert-id').text
        url_redirect = self.live_server_url + reverse('home:home')

        self.assertEqual(
            'Você não tem permissão de acessar está página.',
            message
        )
        self.assertEqual(url_redirect, self.browser.current_url)

    def test_client_client_person_not_found_404(self):
        self.make_login(level='AL')
        url = reverse('client:client', kwargs={'pk': 999})
        self.browser.get(self.live_server_url + url)

        message = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Not Found', message)

    def test_client_client_empty_title_error_message(self):
        def callback(form):
            title = form.find_element(By.NAME, 'title')
            title.clear()
            title.send_keys(' ')
            form.submit()

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            url = reverse('client:client', kwargs={'pk': self.person.id})
            url = reverse('client:client', kwargs={'pk': self.person.id})
            url_redirect = self.live_server_url + url

            self.assertIn('Prencha o campo de titulo.', message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)

    def test_client_client_empty_content_error_message(self):
        def callback(form):
            content = form.find_element(By.NAME, 'content')
            content.clear()
            content.send_keys(' ')
            form.submit()

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            url = reverse('client:client', kwargs={'pk': self.person.id})
            url_redirect = self.live_server_url + url

            self.assertIn('Prencha o campo de conteudo.', message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)

    def test_client_client_empty_due_date_error_message(self):
        def callback(form):
            due_date = form.find_element(By.NAME, 'due_date')
            due_date.send_keys((Keys.BACKSPACE + Keys.RIGHT) * 6)
            form.submit()

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            url = reverse('client:client', kwargs={'pk': self.person.id})
            url_redirect = self.live_server_url + url

            self.assertIn('Prencha o campo de data.', message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)

    def test_client_client_empty_discipline_error_message(self):
        def callback(form):
            form.submit()

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            url = reverse('client:client', kwargs={'pk': self.person.id})
            url_redirect = self.live_server_url + url

            self.assertIn('Selecione uma disciplina.', message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)

    def test_client_client_empty_teacher_error_message(self):
        def callback(form):
            form.find_element(By.NAME, 'discipline').send_keys(Keys.DOWN)
            form.submit()

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            url = reverse('client:client', kwargs={'pk': self.person.id})
            url_redirect = self.live_server_url + url

            self.assertIn('Selecione um professor.', message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)

    def test_client_client_empty_status_error_message(self):
        def callback(form):
            form.find_element(By.NAME, 'discipline').send_keys(Keys.DOWN)
            form.find_element(By.NAME, 'teacher').send_keys(Keys.DOWN)
            form.submit()

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            url = reverse('client:client', kwargs={'pk': self.person.id})
            url_redirect = self.live_server_url + url

            self.assertIn('Seleceione o estado da tarefa.', message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)

    def test_client_client_is_success_message_success(self):
        def callback(form):
            form.find_element(By.NAME, 'discipline').send_keys(Keys.DOWN)
            form.find_element(By.NAME, 'teacher').send_keys(Keys.DOWN)
            form.find_element(By.NAME, 'status').send_keys(Keys.DOWN)
            form.submit()

            message = self.browser.find_element(By.ID, 'message-alert-id').text
            url = reverse('client:client', kwargs={'pk': self.person.id})
            url_redirect = self.live_server_url + url

            self.assertIn('Card criado com sucesso.', message)
            self.assertEqual(url_redirect, self.browser.current_url)
        self.form_field_test_with_callback(callback)
