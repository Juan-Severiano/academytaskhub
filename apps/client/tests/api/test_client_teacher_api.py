from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework import test

from ..base_client import ClientBaseTest
from apps.client.models import Teacher


class ClientTeacherAPITest(test.APITestCase, ClientBaseTest):
    def create_superuser(
            self, username='UserAdmin', password='PassAdmin',
            email='testadmin@aluno.ce.gov.br'
    ):
        return User.objects.create_superuser(
            username=username,
            password=password,
            email=email
        )

    def get_jwt_access(self, username='UserAdmin', password='PassAdmin'):
        data = {'username': username, 'password': password}

        url = reverse('auth:token_obtain_pair')
        response = self.client.post(url, data=data)

        return response.data.get('access')

    """
                    ADMIN USER
    """
    def test_client_teacher_api_list_return_status_code_200_success(self):
        self.create_superuser()

        url = reverse('client:teacher-api-list')
        token = f'Bearer {self.get_jwt_access()}'
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_client_teacher_api_retrieve_return_status_code_200_success(self):  # noqa: E501
        self.create_superuser()
        teacher = self.create_teacher()

        url = reverse('client:teacher-api-detail', args=(teacher.id,))
        token = f'Bearer {self.get_jwt_access()}'
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_client_teacher_api_post_return_status_code_201_created(self):
        self.create_superuser()

        url = reverse('client:teacher-api-list')
        token = f'Bearer {self.get_jwt_access()}'
        response = self.client.post(
            url, HTTP_AUTHORIZATION=token, data={'name': 'Teacher'}
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_client_teacher_api_put_return_status_code_200_success(self):
        self.create_superuser()
        teacher = self.create_teacher()
        new_name = 'New Name'

        url = reverse('client:teacher-api-detail', args=(teacher.id,))
        token = f'Bearer {self.get_jwt_access()}'
        response = self.client.put(
            url, HTTP_AUTHORIZATION=token, data={'name': new_name}
        )

        new_teacher = Teacher.objects.get(id=response.data['id'])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(new_teacher.name, new_name)

    def test_client_teacher_api_patch_return_status_code_200_success(self):
        self.create_superuser()
        teacher = self.create_teacher()
        new_name = 'New Name'

        url = reverse('client:teacher-api-detail', args=(teacher.id,))
        token = f'Bearer {self.get_jwt_access()}'
        response = self.client.patch(
            url, HTTP_AUTHORIZATION=token, data={'name': new_name}
        )

        new_teacher = Teacher.objects.get(id=response.data['id'])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(new_teacher.name, new_name)

    def test_client_teacher_api_delete_return_status_code_204_no_content(self):
        self.create_superuser()
        teacher = self.create_teacher()

        url = reverse('client:teacher-api-detail', args=(teacher.id,))
        token = f'Bearer {self.get_jwt_access()}'
        response = self.client.delete(url, HTTP_AUTHORIZATION=token)

        delete_teacher = Teacher.objects.filter(id=teacher.id).exists()

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(delete_teacher, False)

    """
                    COMMON USER
    """
    def test_client_user_teacher_api_list_return_status_code_200_success(self):
        data_user = {'username': 'UserApi', 'password': 'Pass'}
        self.create_user(**data_user)

        url = reverse('client:teacher-api-list')
        token = f'Bearer {self.get_jwt_access(**data_user)}'
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_client_user_teacher_api_retrieve_return_status_code_200_success(self):  # noqa: E501
        data_user = {'username': 'UserApi', 'password': 'Pass'}
        self.create_user(**data_user)
        teacher = self.create_teacher()

        url = reverse('client:teacher-api-detail', args=(teacher.id,))
        token = f'Bearer {self.get_jwt_access(**data_user)}'
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_client_teacher_api_post_return_status_code_401_forbidden(self):
        data_user = {'username': 'UserApi', 'password': 'Pass'}
        self.create_user(**data_user)

        url = reverse('client:teacher-api-list')
        token = f'Bearer {self.get_jwt_access(**data_user)}'
        response = self.client.post(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_client_teacher_api_put_return_status_code_401_forbidden(self):
        data_user = {'username': 'UserApi', 'password': 'Pass'}
        self.create_user(**data_user)

        url = reverse('client:teacher-api-detail', args=(1,))
        token = f'Bearer {self.get_jwt_access(**data_user)}'
        response = self.client.put(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_client_teacher_api_patch_return_status_code_401_forbidden(self):
        data_user = {'username': 'UserApi', 'password': 'Pass'}
        self.create_user(**data_user)

        url = reverse('client:teacher-api-detail', args=(1,))
        token = f'Bearer {self.get_jwt_access(**data_user)}'
        response = self.client.patch(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_client_teacher_api_delete_return_status_code_401_forbidden(self):
        data_user = {'username': 'UserApi', 'password': 'Pass'}
        self.create_user(**data_user)

        url = reverse('client:teacher-api-detail', args=(1,))
        token = f'Bearer {self.get_jwt_access(**data_user)}'
        response = self.client.delete(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    """
                    NOT LOGGED
    """
    def test_client_teacher_api_not_logged_list_return_status_code_401(self):
        url = reverse('client:teacher-api-list')
        response = self.client.get(url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_client_teacher_api_not_logged_retrieve_return_status_code_401(self):  # noqa: E501
        url = reverse('client:teacher-api-detail', args=(1,))
        response = self.client.get(url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_client_teacher_api_not_logged_post_return_status_code_401(self):
        url = reverse('client:teacher-api-list')
        response = self.client.post(url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_client_teacher_api_not_logged_put_return_status_code_401(self):
        url = reverse('client:teacher-api-detail', args=(1,))
        response = self.client.put(url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_client_teacher_api_not_logged_patch_return_status_code_401(self):
        url = reverse('client:teacher-api-detail', args=(1,))
        response = self.client.patch(url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_client_teacher_api_not_logged_delete_return_status_code_401(self):
        url = reverse('client:teacher-api-detail', args=(1,))
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    """
                    OTHERS
    """
    def test_client_teacher_api_return_correct_data(self):
        self.create_superuser()
        teacher = self.create_teacher()

        url = reverse('client:teacher-api-detail', args=(teacher.id,))
        token = f'Bearer {self.get_jwt_access()}'
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(
            {'id': teacher.id, 'name': teacher.name},
            response.data
        )
