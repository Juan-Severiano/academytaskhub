from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from apps.client.models import ItemList
from apps.client.models import Person
from django.utils import timezone


def home(request):
    if request.method == 'GET':
        atual_date = timezone.now().strftime("%Y-%m-%d")

        if request.user.is_authenticated:
            person = Person.objects.get(user=request.user)
            item_list_todo = person.item_list.filter(
                status='TODO').order_by('-due_date')
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
            type='A', status='TODO', root=True).order_by('-due_date')
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
    else:
        messages.error(request, 'Requisição inválida.')
        return redirect(reverse('home:home'))


def to_do(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            person = Person.objects.get(user=request.user)

            item_list_todo = person.item_list.filter(
                status='TODO').order_by('-due_date')

            context = {
                'item_list_todo': item_list_todo,
                'person': person
            }

            return render(
                request, 'pages/to_do.html', context=context)

        item_list_todo = ItemList.objects.filter(
            type='A', status='TODO', root=True).order_by('-due_date')

        context = {'item_list_todo': item_list_todo}
        return render(request, 'pages/to_do.html', context=context)
    else:
        messages.error(request, 'Requisição inválida.')
        return redirect(reverse('home:home'))


def doing(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            person = Person.objects.get(user=request.user)

            item_list_doing = person.item_list.filter(
                status='DOING').order_by('-due_date')

            context = {'item_list_doing': item_list_doing, 'person': person}
            return render(request, 'pages/doing.html', context=context)

        item_list_doing = ItemList.objects.filter(
            type='A', status='DOING', root=True).order_by('-due_date')

        context = {'item_list_doing': item_list_doing}
        return render(request, 'pages/doing.html', context=context)
    else:
        messages.error(request, 'Requisição inválida.')
        return redirect(reverse('home:home'))


def done(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            person = Person.objects.get(user=request.user)

            item_list_done = person.item_list.filter(
                status='DONE').order_by('-due_date')

            context = {'item_list_done': item_list_done, 'person': person}
            return render(request, 'pages/done.html', context=context)

        item_list_done = ItemList.objects.filter(
            type='A', status='DONE', root=True).order_by('-due_date')

        context = {'item_list_done': item_list_done}
        return render(request, 'pages/done.html', context=context)
    else:
        messages.error(request, 'Requisição inválida.')
        return redirect(reverse('home:home'))


def terms(request):
    if request.user.is_authenticated:
        person = Person.objects.get(user=request.user)
        return render(request, 'pages/terms.html', context={'person': person})

    return render(request, 'pages/terms.html')
