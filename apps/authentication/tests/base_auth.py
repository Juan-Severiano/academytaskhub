from django.test import TestCase
from django.contrib.auth.models import User
from apps.client.models import Discipline, ItemList, Person, Teacher
from django.utils import timezone


class AuthBaseTest(TestCase):
    def login_user_person(self):
        username = 'TestUser'
        password = 'Pass'

        self.user = self.create_user(username, password)
        self.login_user(username, password)
        self.person = self.create_person(self.user, 'AD')

    def create_user(
            self,
            username='User',
            password='Pass',
            email='emailtest@gmail.com'
    ):
        return User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )

    def login_user(
            self,
            username='UserTest',
            password='Pass',
    ):
        return self.client.login(
            username=username,
            password=password
        )

    def create_person(
            self, user, level
    ):
        return Person.objects.create(
            user=user,
            level=level
        )

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
            author=None,
            discipline=None,
            teacher=None,
            title='TitleTest',
            content='Content Test',
            due_date=timezone.now(),
            status='TODO',
            type='P',
            root=False
    ):
        if author is None:
            author = {}

        return ItemList.objects.create(
            author=self.create_user(**author),
            title=title,
            content=content,
            due_date=due_date,
            discipline=self.create_discipline(),
            teacher=self.create_teacher(),
            status=status,
            type=type,
            root=root
        )
