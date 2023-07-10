from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized


class ClientURLsTest(TestCase):
    @parameterized.expand([
        ('client', '/client/1/', {'pk': 1}),
        ('admin', '/client/admin/', {}),
        ('cards', '/client/cards/1/', {'pk': 1}),
        (
            'delete_card', '/client/delete_card/1/1/',
            {'pk_card': 1, 'pk_person': 1}
        ),
        (
            'update_card', '/client/update_card/1/1/',
            {'pk_card': 1, 'pk_person': 1}
        ),
    ])
    def test_client_url_is_correct(self, url_name, path, data):
        url = reverse(url_name, kwargs=data)
        self.assertEqual(url, path)
