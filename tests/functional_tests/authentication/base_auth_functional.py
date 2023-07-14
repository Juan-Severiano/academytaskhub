import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_edge_browser
from django.contrib.auth.models import User
from apps.client.models import Person
from django.urls import reverse
from selenium.webdriver.common.by import By


class AuthBaseTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_edge_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, qtd=10):
        time.sleep(qtd)

    def create_user(
            self, username='User', password='Pass',
            email='test@aluno.ce.gov.br',
    ):
        return User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )

    def create_person(self, user=None, level='AD'):
        if user is None:
            user = {}

        return Person.objects.create(
            user=self.create_user(**user),
            level=level
        )

    def make_login(self):
        self.create_person({
            'username': 'UserLogin',
            'password': 'Pass',
            'email': 'userlogin@aluno.ce.gov.br'
        })

        url = reverse('auth:login')
        self.browser.get(self.live_server_url + url)

        form = self.browser.find_element(
            By.XPATH, '/html/body/section/main/form'
        )

        form.find_element(By.NAME, 'email').send_keys(
            'userlogin@aluno.ce.gov.br')
        form.find_element(By.NAME, 'password').send_keys('Pass')

        form.submit()
