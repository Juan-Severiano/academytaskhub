from django.urls import reverse
from .base_home import HomeBaseTest
from apps.client.models import Person


class HomeViewTermsTest(HomeBaseTest):
    def test_home_view_home_returns_correct_person(self):
        self.create_and_login()
        person = Person.objects.get(id=self.person.id)

        url = reverse('home:terms')
        response = self.client.get(url)
        context = response.context['person']

        self.assertIs(person.id, context.id)
