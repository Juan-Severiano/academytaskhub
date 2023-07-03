from django.shortcuts import render
from apps.client.models import ItemList
from datetime import datetime
from apps.client.models import Person


def home(request):
    if request.method == 'GET':
        atual_date = datetime.today().strftime("%Y-%m-%d")

        if request.user.is_authenticated:
            person = Person.objects.get(user=request.user)
            item_list_todo = person.item_list.filter(
                status='TODO').order_by('due_date')
            item_list_doing = person.item_list.filter(
                status='DOING').order_by('-due_date')
            item_list_done = person.item_list.filter(
                status='DONE').order_by('-due_date')

            return render(request, 'pages/home.html', context={
                'atual_date': atual_date,
                'item_list_todo': item_list_todo,
                'item_list_done': item_list_done,
                'item_list_doing': item_list_doing,
                'person': person,
            })

        item_list_todo = ItemList.objects.filter(
            type='A', status='TODO', root=True).order_by('due_date')
        item_list_doing = ItemList.objects.filter(
            type='A', status='DOING', root=True).order_by('-due_date')
        item_list_done = ItemList.objects.filter(
            type='A', status='DONE', root=True).order_by('-due_date')

        return render(request, 'pages/home.html', context={
            'atual_date': atual_date,
            'item_list_todo': item_list_todo,
            'item_today': item_list_doing,
            'item_list_done': item_list_done,
        })


def to_do(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            person = Person.objects.get(user=request.user)

            item_list_todo = person.item_list.filter(
                status='TODO').order_by('due_date')

            return render(request, 'pages/to_do.html',
                          context={'item_list_todo': item_list_todo})

        item_list_todo = ItemList.objects.filter(
            type='A', status='TODO', root=True).order_by('due_date')

        return render(request, 'pages/to_do.html',
                      context={'item_list_todo': item_list_todo})


def doing(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            person = Person.objects.get(user=request.user)

            item_list_doing = person.item_list.filter(
                status='DOING').order_by('-due_date')

            return render(request, 'pages/doing.html',
                          context={'item_list_doing': item_list_doing})

        item_list_doing = ItemList.objects.filter(
            type='A', status='DOING', root=True).order_by('-due_date')

        return render(request, 'pages/doing.html',
                      context={'item_list_doing': item_list_doing})


def done(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            person = Person.objects.get(user=request.user)

            item_list_done = person.item_list.filter(
                status='DONE').order_by('-due_date')

            return render(request, 'pages/done.html',
                          context={'item_list_done': item_list_done})

        item_list_done = ItemList.objects.filter(
            type='A', status='DONE', root=True).order_by('-due_date')

        return render(request, 'pages/done.html',
                      context={'item_list_done': item_list_done})
