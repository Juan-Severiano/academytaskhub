import pytz
from datetime import datetime

from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from apps.validation import validation
from apps.client.models import Person, Discipline, Teacher, ItemList


@login_required(login_url='/auth/login/', redirect_field_name='next')
def admin(request):
    person = Person.objects.get(user=request.user)
    if not person.level == 'AD':
        message = 'Você não tem permissão de acessar está página.'
        messages.error(request, message)
        return redirect(reverse('home:home'))

    if request.method == 'GET':
        disciplines = Discipline.objects.all()
        teachers = Teacher.objects.all()
        status = ItemList.STATUS

        data = request.session.get('admin_form_data', None)
        if data is not None:
            data['discipline'] = int(data.get('discipline', '-1'))
            data['teacher'] = int(data.get('teacher', '-1'))

        return render(request, 'pages/admin.html', context={
            'disciplines': disciplines, 'teachers': teachers,
            'status': status, 'person': person, 'data': data
            })

    elif request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        due_date = request.POST.get('due_date')
        discipline_id = request.POST.get('discipline')
        teacher_id = request.POST.get('teacher')
        status = request.POST.get('status')

        request.session['admin_form_data'] = request.POST

        try:
            discipline = Discipline.objects.filter(id=discipline_id).first()
            teacher = Teacher.objects.filter(id=teacher_id).first()

            if not validation.card_id_valid(
                    request, title, content, due_date,
                    discipline, teacher, status):
                return redirect(reverse('client:admin'))

            add_card_person(
                request.user, title, content, due_date,
                discipline, teacher, status
            )
            message_success = (
                'Card criado e adicionado a todos os alunos com sucesso.'
            )
            messages.success(request, message_success)
            del (request.session['admin_form_data'])
            return redirect(reverse('client:admin'))
        except Exception as e:
            messages.error(request, f'Erro interno do sistema: {str(e)}')
            return redirect(reverse('client:admin'))
    else:
        messages.error(request, 'Requisição inválida.')
        return redirect(reverse('home:home'))


def add_card_person(
        author, title, content, due_date,
        discipline, teacher, status, type='A'
):
    people = Person.objects.filter(level='AL') \
        .prefetch_related('item_list').select_related('user')
    people = people.union(
        Person.objects.filter(level='AD')
        .prefetch_related('item_list').select_related('user')
    )

    due_date_formated = datetime.strptime(due_date, "%Y-%m-%dT%H:%M")
    fuso_horario = pytz.timezone(settings.TIME_ZONE)
    date = due_date_formated.replace(tzinfo=pytz.utc).astimezone(fuso_horario)

    for person in people:
        root = False
        if author.id == person.user.id:
            root = True

        item_list = ItemList.objects.create(
            author=author,
            title=title,
            content=content,
            due_date=date,
            discipline=discipline,
            teacher=teacher,
            status=status,
            type=type,
            root=root
        )
        item_list.save()
        person.item_list.add(item_list)
