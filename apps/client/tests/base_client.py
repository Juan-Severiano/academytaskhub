from django.test import TestCase
from django.contrib.auth.models import User
from apps.client.models import ItemList, Discipline, Teacher, Person
from django.utils import timezone


class ClientBaseTest(TestCase):
    def setUp(self) -> None:
        self.username = 'UserTest',
        self.password = 'Pass'

        self.user = self.create_user(
            self.username,
            self.password
        )
        self.person = self.create_person(
            self.user, level='AD'
        )
        self.login = self.login_user(
            self.username,
            self.password
        )
        return super().setUp()

    def create_user(
            self, username, password='Pass'
    ):
        return User.objects.create_user(
            username=username,
            password=password
        )

    def login_user(
            self, username, password
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
    ):
        return ItemList.objects.create(
            author=self.user,
            title=title,
            content=content,
            due_date=due_date,
            discipline=self.create_discipline(),
            teacher=self.create_teacher(),
            status=status,
            type=type,
        )
