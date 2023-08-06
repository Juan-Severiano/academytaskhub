from parameterized import parameterized
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import test
from rest_framework import status
from ..base_auth import AuthBaseTest


class AuthAPITest(test.APITestCase, AuthBaseTest):
    def create_superuser(
            self, username='UserAdmin', password='PassAdmin',
            email='testadmin@aluno.ce.gov.br'
    ):
        return User.objects.create_superuser(
            username=username,
            password=password,
            email=email
        )

    def get_data(self):
        return {
            'username': 'test',
            'email': 'test@aluno.ce.gov.br',
            'password': 'senha123',
            'confirm_password': 'senha123'
        }

    def get_jwt_access(self, username='UserAdmin', password='PassAdmin'):
        data = {'username': username, 'password': password}

        url = reverse('auth:token_obtain_pair')
        response = self.client.post(url, data=data)

        return response.data.get('access')

    """
                    ADMIN USER
    """
    def test_auth_api_admin_list_return_status_code_200(self):
        username, password = 'UserApi', 'Pass'
        self.create_superuser(username, password)

        url = reverse('auth:user-api-list')
        token = f'Bearer {self.get_jwt_access(username, password)}'
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=token
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_auth_api_admin_retrieve_return_status_code_200(self):
        data_admin = {'username': 'UserAdmin', 'password': 'PassAdmin'}
        self.create_superuser(**data_admin)

        data = {'username': 'User', 'password': 'Pass'}
        user = self.create_user(**data)

        url = reverse('auth:user-api-detail', args=(user.id, ))
        token = f'Bearer {self.get_jwt_access(**data_admin)}'
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    @parameterized.expand([
        'username',
        'email',
        'password',
        'confirm_password'
    ])
    def test_auth_api_admin_post_return_field_required(self, field):
        self.create_superuser()

        url = reverse('auth:user-api-list')
        token = f'Bearer {self.get_jwt_access()}'

        response = self.client.post(url, data={}, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            'Este campo é obrigatório.',
            response.data.get(field)[0]
        )

    @parameterized.expand([
        'username',
        'email',
        'password',
        'confirm_password'
    ])
    def test_auth_api_admin_post_return_cannot_be_blank(self, field):
        self.create_superuser()

        url = reverse('auth:user-api-list')
        token = f'Bearer {self.get_jwt_access()}'

        data = {field: ' '}
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            'Este campo não pode ser em branco.',
            response.data.get(field)[0]
        )

    def test_auth_api_admin_post_return_username_already_used(self):
        user = self.create_superuser()

        url = reverse('auth:user-api-list')
        token = f'Bearer {self.get_jwt_access()}'

        data = {'username': user.username}
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            'Um usuário com este nome de usuário já existe.',
            response.data.get('username')[0]
        )

    def test_auth_api_admin_post_return_email_is_not_valid(self):
        self.create_superuser()

        url = reverse('auth:user-api-list')
        token = f'Bearer {self.get_jwt_access()}'

        data = {'email': 'invalid'}
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            'Insira um endereço de email válido.',
            response.data.get('email')[0]
        )

    def test_auth_api_admin_post_return_email_must_be_from_gov(self):
        self.create_superuser()

        url = reverse('auth:user-api-list')
        token = f'Bearer {self.get_jwt_access()}'

        data = self.get_data()
        data['email'] = 'ivalid@gmail.com'
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            'O email precisa ser do gov.br.',
            response.data.get('email')[0]
        )

    def test_auth_api_admin_post_return_email_already_used(self):
        user = self.create_superuser()

        url = reverse('auth:user-api-list')
        token = f'Bearer {self.get_jwt_access()}'

        data = self.get_data()
        data['email'] = user.email
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            'Email já utilizado.',
            response.data.get('email')[0]
        )

    def test_auth_api_admin_post_return_passwords_not_match(self):
        self.create_superuser()

        url = reverse('auth:user-api-list')
        token = f'Bearer {self.get_jwt_access()}'

        data = self.get_data()
        data['confirm_password'] = 'invalid'
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            'As senhas não coicidem.',
            response.data.get('password')[0]
        )
        self.assertEqual(
            'As senhas não coicidem.',
            response.data.get('confirm_password')[0]
        )

    @parameterized.expand([
        'username',
        'email',
        'password',
        'confirm_password'
    ])
    def test_auth_api_admin_patch_return_cannot_be_blank(self, field):
        self.create_superuser()
        card = self.create_card()

        url = reverse('auth:user-api-detail', args=(card.id,))
        token = f'Bearer {self.get_jwt_access()}'

        data = {field: ' '}
        response = self.client.patch(url, data=data, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            'Este campo não pode ser em branco.',
            response.data.get(field)[0]
        )

    def test_auth_api_admin_patch_return_email_must_be_from_gov(self):
        self.create_superuser()
        card = self.create_card()

        url = reverse('auth:user-api-detail', args=(card.id,))
        token = f'Bearer {self.get_jwt_access()}'

        data = {'email': 'invalid@gmail.com'}
        response = self.client.patch(url, data=data, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            'O email precisa ser do gov.br.',
            response.data.get('email')[0]
        )

    def test_auth_api_admin_patch_return_confirm_password_cannot_blank(self):
        self.create_superuser()
        card = self.create_card()

        url = reverse('auth:user-api-detail', args=(card.id,))
        token = f'Bearer {self.get_jwt_access()}'

        data = {}
        response = self.client.patch(url, data=data, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            'Prencha o campo de confirmar senha.',
            response.data.get('confirm_password')[0]
        )

    def test_auth_api_admin_patch_return_passwords_not_match(self):
        self.create_superuser()
        card = self.create_card()

        url = reverse('auth:user-api-detail', args=(card.id,))
        token = f'Bearer {self.get_jwt_access()}'

        data = self.get_data()
        data['password'] = 'invalid'
        response = self.client.patch(url, data=data, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            'As senhas não coicidem.',
            response.data.get('password')[0]
        )
        self.assertEqual(
            'As senhas não coicidem.',
            response.data.get('confirm_password')[0]
        )

    def test_auth_api_admin_patch_return_status_code_201(self):
        data_admin = {'username': 'UserAdmin', 'password': 'PassAdmin'}
        self.create_superuser(**data_admin)

        card = self.create_card()

        url = reverse('auth:user-api-detail', args=(card.id,))
        token = f'Bearer {self.get_jwt_access(**data_admin)}'
        response = self.client.patch(
            url,
            data=self.get_data(),
            HTTP_AUTHORIZATION=token
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_auth_api_admin_delte_return_status_code_204(self):
        data_admin = {'username': 'UserAdmin', 'password': 'PassAdmin'}
        self.create_superuser(**data_admin)

        card = self.create_card()

        url = reverse('auth:user-api-detail', args=(card.id,))
        token = f'Bearer {self.get_jwt_access(**data_admin)}'
        response = self.client.delete(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    """
                    COMMON USER
    """
    def test_auth_api_user_list_return_status_code_403(self):
        username, password = 'UserApi', 'Pass'
        self.create_user(username, password)

        url = reverse('auth:user-api-list')
        token = f'Bearer {self.get_jwt_access(username, password)}'
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(
            'Você não tem permissão para executar essa ação.',
            response.data.get('detail')
        )

    def test_auth_api_user_retrieve_return_status_code_200(self):
        data = {'username': 'User', 'password': 'Pass'}
        user = self.create_user(**data)

        url = reverse('auth:user-api-detail', args=(user.id, ))
        token = f'Bearer {self.get_jwt_access(**data)}'
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_auth_api_user_retrieve_return_status_code_403(self):
        data = {'username': 'UserTest', 'password': 'Pass'}
        self.create_user(**data)

        user = {'username': 'UserCard', 'password': 'PassCard'}
        user = self.create_user(**user)

        url = reverse('auth:user-api-detail', args=(user.id, ))
        token = f'Bearer {self.get_jwt_access(**data)}'
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(
            'Você não tem permissão para executar essa ação.',
            response.data.get('detail')
        )

    def test_auth_api_user_post_return_status_code_403(self):
        data = {'username': 'UserTest', 'password': 'Pass'}
        self.create_user(**data)

        url = reverse('auth:user-api-list')
        token = f'Bearer {self.get_jwt_access(**data)}'
        response = self.client.post(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(
            'Você não tem permissão para executar essa ação.',
            response.data.get('detail')
        )

    def test_auth_api_user_patch_return_status_code_403(self):
        data = {'username': 'UserTest', 'password': 'Pass'}
        self.create_user(**data)

        url = reverse('auth:user-api-detail', args=(1,))
        token = f'Bearer {self.get_jwt_access(**data)}'
        response = self.client.patch(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(
            'Você não tem permissão para executar essa ação.',
            response.data.get('detail')
        )

    def test_auth_api_user_delete_return_status_code_403(self):
        data = {'username': 'UserTest', 'password': 'Pass'}
        self.create_user(**data)

        url = reverse('auth:user-api-detail', args=(1,))
        token = f'Bearer {self.get_jwt_access(**data)}'
        response = self.client.delete(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(
            'Você não tem permissão para executar essa ação.',
            response.data.get('detail')
        )

    """
                    NOT LOGGED
    """
    def test_auth_api_not_logged_list_return_status_code_401(self):
        url = reverse('auth:user-api-list')
        response = self.client.get(url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_auth_api_not_logged_retrieve_return_status_code_401(self):
        url = reverse('auth:user-api-detail', args=(1,))
        response = self.client.get(url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_auth_api_not_logged_post_return_status_code_401(self):
        url = reverse('auth:user-api-list')
        response = self.client.post(url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_auth_api_put_return_status_code_405(self):
        self.create_superuser()

        url = reverse('auth:user-api-detail', args=(1,))
        token = f'Bearer {self.get_jwt_access()}'
        response = self.client.put(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(405, response.status_code)

    def test_auth_api_not_logged_patch_return_status_code_401(self):
        url = reverse('auth:user-api-detail', args=(1,))
        response = self.client.patch(url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_auth_api_not_logged_delete_return_status_code_401(self):
        url = reverse('auth:user-api-detail', args=(1,))
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    """
                    OTHERS
    """
    def test_auth_api_user_not_active(self):
        user = self.create_user()
        user.is_active = False
        user.save()

        url = reverse('auth:token_obtain_pair')
        response = self.client.post(url, data={
            'username': 'User',
            'password': 'Pass'
        })

        message = (
            'Você ainda não ativou sua conta no email. '
            'Acabamos de lhe enviar outro email.'
        )

        self.assertEqual(message, response.data[0])
