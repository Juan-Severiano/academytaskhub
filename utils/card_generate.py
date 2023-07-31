from apps.client.models import ItemList
from utils.person_generate import get_person_list


def copy_card(item):
    item_copy = ItemList.objects.create(
        author=item.author,
        title=item.title,
        content=item.content,
        due_date=item.due_date,
        discipline=item.discipline,
        teacher=item.teacher,
        status=item.status,
        type=item.type
    )
    return item_copy


def add_card_person(
        author, title, content, due_date,
        discipline, teacher, status, type='A'
):
    people = get_person_list(level='AL')
    people = people.union(get_person_list(level='AD'))

    for person in people:
        root = False
        if author.id == person.user.id:
            root = True

        item_list = ItemList.objects.create(
            author=author,
            title=title,
            content=content,
            due_date=due_date,
            discipline=discipline,
            teacher=teacher,
            status=status,
            type=type,
            root=root
        )
        item_list.save()
        person.item_list.add(item_list)


def get_items_list(entity, **kwargs):
    entity = entity.objects if entity is ItemList else entity.item_list

    item_list = entity.filter(**kwargs) \
        .order_by('-due_date') \
        .select_related('author', 'discipline', 'teacher')

    to_do = item_list.filter(status='TODO')
    doing = item_list.filter(status='DOING')
    done = item_list.filter(status='DONE')

    return to_do, doing, done


def get_item_list(entity, **kwargs):
    entity = entity.objects if entity is ItemList else entity.item_list

    item_list = entity.filter(**kwargs) \
        .order_by('-due_date') \
        .select_related('author', 'discipline', 'teacher')

    return item_list
