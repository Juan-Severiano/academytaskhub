from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect

from apps.client.models import Person, ItemList
from utils.card_generate import get_item_list, get_items_list


def home(request):
    if request.method == 'GET':
        atual_date = timezone.now().strftime("%Y-%m-%d")

        if request.user.is_authenticated:
            person = Person.objects.get(user=request.user)

            to_do, doing, done = get_items_list(person)

            return render(request, 'pages/home.html', context={
                'atual_date': atual_date, 'item_list_todo': to_do,
                'item_list_doing': doing, 'item_list_done': done,
                'person': person,
            })

        to_do, doing, done = get_items_list(ItemList, type='A', root=True)

        return render(request, 'pages/home.html', context={
            'atual_date': atual_date, 'item_list_todo': to_do,
            'item_list_doing': doing, 'item_list_done': done,
        })
    else:
        messages.error(request, 'Requisição inválida.')
        return redirect(reverse('home:home'))


def specific_status(request, status):
    status = status.upper()
    STATUS = [status[0] for status in ItemList.STATUS]

    if status not in STATUS:
        messages.error(request, 'status inválido.')
        return redirect(reverse('home:home'))

    if request.method == 'GET':
        if request.user.is_authenticated:
            person = Person.objects.get(user=request.user)
            item_list = get_item_list(person, status=status)

            context = {
                'item_list': item_list,
                'person': person, 'stauts': status
            }
            return render(
                request, 'pages/specific_status.html', context=context
            )

        item_list = get_item_list(ItemList, type='A', status=status, root=True)

        context = {'item_list': item_list, 'stauts': status}
        return render(request, 'pages/specific_status.html', context=context)
    else:
        messages.error(request, 'Requisição inválida.')
        return redirect(reverse('home:home'))


def terms(request):
    if request.user.is_authenticated:
        person = Person.objects.get(user=request.user)
        return render(request, 'pages/terms.html', context={'person': person})

    return render(request, 'pages/terms.html')
