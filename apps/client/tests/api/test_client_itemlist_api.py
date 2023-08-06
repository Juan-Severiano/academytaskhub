from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework import test

from ..base_client import ClientBaseTest
from apps.client.models import Person, ItemList


class ClientItemListAPITest(test.APITestCase, ClientBaseTest):
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

    def get_data(self):
        return {
            'title': 'Titulo',
            'content': 'Content',
            'due_date': '2023-08-05',
            'discipline': self.create_discipline().id,
            'teacher': self.create_teacher().id,
            'status': 'TODO',
            'type': 'P'
        }
    """
                    ADMIN USER
    """
    def test_client_adm_itemlist_api_list_return_status_code_200_success(self):
        self.create_superuser()
        qtd_card = 3
        for i in range(qtd_card):
            self.create_card()

        url = reverse('client:itemlist-api-list')
        token = f'Bearer {self.get_jwt_access()}'
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(qtd_card, response.data['count'])

    def test_client_adm_itemlist_api_retrieve_return_status_code_200_success(self):  # noqa: E501
        self.create_superuser()
        card = self.create_card()

        url = reverse('client:itemlist-api-detail', args=(card.id,))
        token = f'Bearer {self.get_jwt_access()}'
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_client_adm_itemlist_api_post_return_status_code_201_created(self):
        user = self.create_superuser()
        person = self.create_person(user, 'AD')

        url = reverse('client:itemlist-api-list')
        token = f'Bearer {self.get_jwt_access()}'
        response = self.client.post(
            url, HTTP_AUTHORIZATION=token, data=self.get_data()
        )

        person = Person.objects.get(id=person.id)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(person.item_list.first().id, response.data['id'])

    def test_client_adm_itemlist_api_put_return_status_code_200_success(self):
        NEW_TITLE = 'New Title'

        self.create_superuser()
        card = self.create_card()
        data = self.get_data()
        data['title'] = NEW_TITLE

        url = reverse('client:itemlist-api-detail', args=(card.id,))
        token = f'Bearer {self.get_jwt_access()}'
        response = self.client.put(url, HTTP_AUTHORIZATION=token, data=data)

        new_itemlist = ItemList.objects.get(id=response.data['id'])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(new_itemlist.title, NEW_TITLE)

    def test_client_adm_itemlist_api_patch_return_status_code_200_success(self):  # noqa: E501
        NEW_TITLE = 'New Title'

        self.create_superuser()
        card = self.create_card()

        url = reverse('client:itemlist-api-detail', args=(card.id,))
        token = f'Bearer {self.get_jwt_access()}'
        response = self.client.patch(
            url, HTTP_AUTHORIZATION=token, data={'title': NEW_TITLE}
        )

        new_itemlist = ItemList.objects.get(id=response.data['id'])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(new_itemlist.title, NEW_TITLE)

    def test_client_adm_itemlist_api_delete_return_status_code_204_no_content(self):  # noqa: E501
        self.create_superuser()
        card = self.create_card()

        url = reverse('client:itemlist-api-detail', args=(card.id,))
        token = f'Bearer {self.get_jwt_access()}'
        response = self.client.delete(url, HTTP_AUTHORIZATION=token)

        delete_itemlist = ItemList.objects.filter(id=card.id).exists()

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(delete_itemlist, False)

    """
                    COMMON USER
    """
    def test_clien_usert_itemlist_api_list_return_status_code_200_success(self):  # noqa: E501
        data_user = {'username': 'UserApi', 'password': 'Pass'}
        self.user = self.create_user(**data_user)
        self.create_card()

        url = reverse('client:itemlist-api-list')
        token = f'Bearer {self.get_jwt_access(**data_user)}'
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, response.data['count'])
        self.assertEqual(
            self.user.id, response.data['results'][0]['author']['id']
        )

    def test_client_user_itemlist_api_retrieve_return_status_code_200_success(self):  # noqa: E501
        self.client.logout()
        data_user = {'username': 'UserApi', 'password': 'Pass'}
        self.user = self.create_user(**data_user)
        card = self.create_card()

        url = reverse('client:itemlist-api-detail', args=(card.id,))
        token = f'Bearer {self.get_jwt_access(**data_user)}'
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            self.user.id, response.data['author']['id']
        )

    def test_client_user_itemlist_api_post_return_status_code_201_created(self):  # noqa: 501
        data_user = {'username': 'UserApi', 'password': 'Pass'}
        user = self.create_user(**data_user)
        person = self.create_person(user, 'AL')

        url = reverse('client:itemlist-api-list')
        token = f'Bearer {self.get_jwt_access(**data_user)}'
        response = self.client.post(
            url, HTTP_AUTHORIZATION=token, data=self.get_data()
        )

        person = Person.objects.get(id=person.id)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(person.item_list.first().id, response.data['id'])

    def test_client_user_itemlist_api_put_return_status_code_200_success(self):  # noqa: 501
        data_user = {'username': 'UserApi', 'password': 'Pass'}
        self.user = self.create_user(**data_user)
        card = self.create_card()

        url = reverse('client:itemlist-api-detail', args=(card.id,))
        token = f'Bearer {self.get_jwt_access(**data_user)}'
        response = self.client.put(
            url, HTTP_AUTHORIZATION=token, data=self.get_data()
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_client_user_itemlist_api_patch_return_status_code_200_success(self):  # noqa: 501
        data_user = {'username': 'UserApi', 'password': 'Pass'}
        self.user = self.create_user(**data_user)
        card = self.create_card()
        new_title = 'New title'

        url = reverse('client:itemlist-api-detail', args=(card.id,))
        token = f'Bearer {self.get_jwt_access(**data_user)}'
        response = self.client.patch(
            url, HTTP_AUTHORIZATION=token, data={'title': new_title}
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(new_title, response.data['title'])

    def test_client_user_itemlist_api_delete_return_status_code_204_no_content(self):  # noqa: E501
        data_user = {'username': 'UserApi', 'password': 'Pass'}
        card = self.create_card(author=data_user)

        url = reverse('client:itemlist-api-detail', args=(card.id,))
        token = f'Bearer {self.get_jwt_access(**data_user)}'
        response = self.client.delete(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    """
                    NOT LOGGED
    """
    def test_client_itemlist_api_not_logged_list_return_status_code_401(self):
        url = reverse('client:itemlist-api-list')
        response = self.client.get(url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_client_itemlist_api_not_logged_retrieve_return_status_code_401(self):  # noqa: E501
        url = reverse('client:itemlist-api-detail', args=(1,))
        response = self.client.get(url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_client_itemlist_api_not_logged_post_return_status_code_401(self):
        url = reverse('client:itemlist-api-list')
        response = self.client.post(url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_client_itemlist_api_not_logged_put_return_status_code_401(self):
        url = reverse('client:itemlist-api-detail', args=(1,))
        response = self.client.put(url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_client_itemlist_api_not_logged_patch_return_status_code_401(self):  # noqa: E501
        url = reverse('client:itemlist-api-detail', args=(1,))
        response = self.client.patch(url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_client_itemlist_api_not_logged_delete_return_status_code_401(self):  # noqa: E501
        url = reverse('client:itemlist-api-detail', args=(1,))
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    """
                    OTHERS
    """
    def test_client_itemlist_api_not_is_owner_itemlist(self):
        data_user = {'username': 'UserApi', 'password': 'Pass'}
        self.create_user(**data_user)
        card = self.create_card({'username': 'OtherUser', 'password': 'Pass'})

        url = reverse('client:itemlist-api-detail', args=(card.id, ))
        token = f'Bearer {self.get_jwt_access(**data_user)}'
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
