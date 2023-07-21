import pytz
from datetime import datetime

from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from apps.validation import validation
from apps.client.models import Person, Discipline, Teacher, ItemList


@login_required(login_url='/auth/login/', redirect_field_name='next')
def cards(request, pk):
    if request.method == 'GET':
        person = get_object_or_404(Person, id=pk)
        user = get_object_or_404(Person, user=request.user)

        if not user.id == person.id:
            message = 'Você não tem permissão de acessar está página.'
            messages.error(request, message)
            return redirect(reverse('home:home'))

        person = Person.objects.get(user=request.user)
        atual_date = timezone.now().strftime("%Y-%m-%d")

        item_list = person.item_list.order_by('-due_date') \
            .select_related('author', 'discipline', 'teacher')
        item_list_todo = item_list.filter(status='TODO')
        item_list_doing = item_list.filter(status='DOING')
        item_list_done = item_list.filter(status='DONE')

        return render(request, 'pages/cards.html', context={
            'atual_date': atual_date,
            'item_list_todo': item_list_todo,
            'item_list_done': item_list_done,
            'item_list_doing': item_list_doing,
            'person': person,
        })
    else:
        messages.error(request, 'Requisição inválida.')
        return redirect(reverse('home:home'))


@login_required(login_url='/auth/login/', redirect_field_name='next')
def delete_card(request, pk_card, pk_person):
    if request.method == 'GET':
        person = get_object_or_404(Person, id=pk_person)
        user = get_object_or_404(Person, user=request.user)

        if not user.id == person.id:
            message = 'Você não tem permissão de acessar está página.'
            messages.error(request, message)
            return redirect(reverse('home:home'))

        card = get_object_or_404(ItemList, id=pk_card)
        card.delete()
        messages.success(request, 'Card deletado com sucesso.')
        return redirect(reverse('client:cards', kwargs={'pk': person.id}))
    else:
        messages.error(request, 'Requisição inválida.')
        return redirect(reverse('home:home'))


@login_required(login_url='/auth/login/', redirect_field_name='next')
def update_card(request, pk_card, pk_person):
    person = get_object_or_404(Person, id=pk_person)
    user = get_object_or_404(Person, user=request.user)
    card = get_object_or_404(ItemList, id=pk_card)

    data = {
        'pk_card': card.id,
        'pk_person': person.id
    }

    if not user.id == person.id:
        message = 'Você não tem permissão de acessar está página.'
        messages.error(request, message)
        return redirect(reverse('home:home'))

    if request.method == 'GET':
        disciplines = Discipline.objects.all()
        teachers = Teacher.objects.all()

        date = card.due_date.strftime("%Y-%m-%dT%H:%M")

        return render(request, 'pages/update_card.html', context={
            'card': card,
            'person': person,
            'disciplines': disciplines,
            'teachers': teachers,
            'date': date,
        })

    elif request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        due_date = request.POST.get('due-date')
        discipline_id = request.POST.get('discipline')
        teacher_id = request.POST.get('teacher')
        status = request.POST.get('status')

        try:
            discipline = get_object_or_404(Discipline, id=discipline_id)
            teacher = get_object_or_404(Teacher, id=teacher_id)

            if not validation.card_id_valid(
                request, title, content, due_date, discipline, teacher, status
            ):
                return redirect(reverse('client:update_card', kwargs=data))

            due_date_formated = datetime.strptime(due_date, "%Y-%m-%dT%H:%M")
            fuso_horario = pytz.timezone(settings.TIME_ZONE)
            date = due_date_formated.replace(
                tzinfo=pytz.utc
            ).astimezone(fuso_horario)

            card.title = title
            card.content = content
            card.due_date = date
            card.discipline = discipline
            card.teacher = teacher
            card.status = status
            card.save()
            messages.success(request, 'Tarefa atualizada com sucesso.')
            return redirect(reverse('client:cards', kwargs={'pk': person.id}))
        except Exception as e:
            messages.error(request, f'Erro interno no sistema: {str(e)}')
            return redirect(reverse('client:update_card', kwargs=data))
    else:
        messages.error(request, 'Requisição inválida.')
        return redirect(reverse('home:home'))
