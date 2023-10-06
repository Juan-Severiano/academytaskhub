from django.shortcuts import get_object_or_404
from apps.client.models import Person


def get_person_list(**kwargs):
    people = Person.objects.filter(**kwargs) \
        .select_related('user') \
        .prefetch_related('item_list')

    return people


def get_person(**kwargs):
    person = get_object_or_404(Person, **kwargs)
    return person
