from django.test import TestCase
from django.contrib.auth.models import User


class AuthBaseTest(TestCase):
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
