from .base_home import HomeBaseTest
from utils.person_generate import get_person


class HomeViewTest(HomeBaseTest):
    def test_home_view_function_get_person_returns_correct_item_list(self):
        self.create_and_login()
        person = get_person(pk=self.person.id)

        self.assertEqual(self.person, person)
