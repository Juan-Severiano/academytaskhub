import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_edge_browser
from django.contrib.auth.models import User
from apps.client.models import Person, Discipline, Teacher, ItemList
from django.urls import reverse
from selenium.webdriver.common.by import By
from django.utils import timezone
import pytz
from django.conf import settings


class ClientBaseTest(StaticLiveServerTestCase):
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

    def make_login(
            self, username='UserLogin', password='Pass',
            email='userlogin@aluno.ce.gov.br',
            level='AD'
    ):
        self.person = self.create_person({
            'username': username,
            'password': password,
            'email': email
        }, level=level)

        url = reverse('auth:login')
        self.browser.get(self.live_server_url + url)

        form = self.browser.find_element(
            By.XPATH, '/html/body/section/main/form'
        )

        form.find_element(By.NAME, 'email').send_keys(
            'userlogin@aluno.ce.gov.br')
        form.find_element(By.NAME, 'password').send_keys('Pass')

        form.submit()

    def create_discipline(
            self, name='Discipline', is_technical_area=False
    ):
        return Discipline.objects.create(
            name=name,
            is_technical_area=is_technical_area
        )

    def create_teacher(
            self, name='Teacher'
    ):
        return Teacher.objects.create(
            name=name
        )

    def create_card(
            self,
            author,
            discipline=None,
            teacher=None,
            title='TitleTest',
            content='Content Test',
            due_date=None,
            status='TODO',
            type='P',
    ):

        fuso_horario = pytz.timezone(settings.TIME_ZONE)
        date = timezone.now().replace(tzinfo=pytz.utc).astimezone(fuso_horario)

        self.card = ItemList.objects.create(
            author=author,
            title=title,
            content=content,
            due_date=date,
            discipline=self.create_discipline(),
            teacher=self.create_teacher(),
            status=status,
            type=type,
        )

        return self.card
