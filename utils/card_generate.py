from apps.client.models import ItemList


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
