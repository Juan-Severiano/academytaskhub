from apps.client.models import Person


def get_person_list(**kwargs):
    item_list = Person.objects.filter(**kwargs) \
        .select_related('user') \
        .prefetch_related('item_list')

    return item_list


def get_person(**kwargs):
    item_list = Person.objects.get(**kwargs)
    return item_list
