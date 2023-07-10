from django.test import TestCase
from django.contrib.auth.models import User
from apps.client.models import ItemList


class AuthBaseTest(TestCase):
    def setUp(self) -> None:
        self.user = self.login_user()
        return super().setUp()

    def create_user(
        self,
        username='UserTest',
        password='Pass',
    ):
        return User.objects.create_user(
            username=username,
            password=password
        )

    def login_user(self):
        username = 'UserTest'
        password = 'Pass'
        self.create_user(
            username=username,
            password=password
        )

        self.client.login(
            username=username,
            password=password
        )

    # def create_card(self):
    #     card = ItemList.objects.create(
    #         author=self.user,
    #         title='Titles Test',
    #         content='Content Test',
    #         due_date=''
    #     )
