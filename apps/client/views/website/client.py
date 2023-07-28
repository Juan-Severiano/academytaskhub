import pytz
from datetime import datetime

from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from apps.validation import validation
from apps.client.models import Person, Discipline, Teacher, ItemList


@login_required(login_url='/auth/login/', redirect_field_name='next')
def client(request, pk):
    person = get_object_or_404(Person, id=pk)
    user = get_object_or_404(Person, user=request.user)
    data = {'pk': person.id}

    if not person.id == user.id:
        message = 'Você não tem permissão de acessar está página.'
        messages.error(request, message)
        return redirect(reverse('home:home'))

    if request.method == 'GET':
        disciplines = Discipline.objects.all()
        teachers = Teacher.objects.all()
        status = ItemList.STATUS

        data = request.session.get('client_form_data', None)
        if data is not None:
            data['discipline'] = int(data.get('discipline', '-1'))
            data['teacher'] = int(data.get('teacher', '-1'))

        return render(request, 'pages/client.html',
                      context={
                          'data': data,
                          'person': person,
                          'disciplines': disciplines,
                          'teachers': teachers,
                          'status': status})

    elif request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        due_date = request.POST.get('due_date')
        discipline_id = request.POST.get('discipline')
        teacher_id = request.POST.get('teacher')
        status = request.POST.get('status')

        request.session['client_form_data'] = request.POST

        try:
            naive_datetime = datetime.strptime(due_date, "%Y-%m-%dT%H:%M")
            target = pytz.timezone(settings.TIME_ZONE)
            aware_datetime = timezone.make_aware(naive_datetime, target)
        except (ValueError, TypeError):
            aware_datetime = due_date

        try:
            discipline = Discipline.objects.filter(id=discipline_id).first()
            teacher = Teacher.objects.filter(id=teacher_id).first()

            if not validation.card_id_valid(
                    request, title,
                    content, due_date,
                    discipline, teacher, status):
                return redirect(reverse('client:client', kwargs=data))

            item_list = ItemList.objects.create(
                author=request.user,
                title=title,
                content=content,
                due_date=aware_datetime,
                discipline=discipline,
                teacher=teacher,
                status=status,
                type='P'
            )
            item_list.save()
            person.item_list.add(item_list)
            messages.success(request, 'Card criado com sucesso.')
            del (request.session['client_form_data'])
            return redirect(reverse('client:client', kwargs=data))
        except Exception as e:
            messages.error(request, f'Erro interno do sistema: {str(e)}')
            return redirect(reverse('client:client', kwargs=data))
    else:
        messages.error(request, 'Requisição inválida.')
        return redirect(reverse('home:home'))
