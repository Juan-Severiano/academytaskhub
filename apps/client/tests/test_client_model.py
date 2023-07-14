from .base_client import ClientBaseTest


class ClientModelTest(ClientBaseTest):
    def test_client_itemlist_model_string_representarion_is_name_field(self):
        card = self.create_card()
        self.assertEqual(str(card), card.title)

    def test_client_person_model_string_representarion_is_name_field(self):
        user = self.create_user(username='Name')
        person = self.create_person(user, level='AL')
        self.assertEqual(str(person), person.user.username)

    def test_client_teacher_model_string_representarion_is_name_field(self):
        teacher = self.create_teacher(name='Teacher')
        self.assertEqual(str(teacher), teacher.name)

    def test_client_discipline_model_string_representarion_is_name_field(self):
        discipline = self.create_discipline(name='Discipline')
        self.assertEqual(str(discipline), discipline.name)
