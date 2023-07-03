from django.shortcuts import render, redirect
from django.contrib import messages
from apps.client.models import Person, Discipline, Teacher, ItemList
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User
from apps.validation import validation


@login_required(login_url='/auth/login')
def admin(request):
    person = Person.objects.get(user=request.user)
    if not person.level == 'AD':
        messages.error(request, 'Você não tem permissão de acessar está página.')
        return redirect('/')

    if request.method == 'GET':       
        disciplines = Discipline.objects.all()
        teachers = Teacher.objects.all()
        status = ItemList.STATUS

        return render(request, 'pages/admin.html', context={
            'disciplines': disciplines, 'teachers': teachers,
            'status': status, 'person': person})

    elif request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        due_date = request.POST.get('due-date')
        discipline_id = request.POST.get('discipline')
        teacher_id = request.POST.get('teacher')
        status = request.POST.get('status')

        try:
            discipline = Discipline.objects.filter(id=discipline_id).first()
            teacher = Teacher.objects.filter(id=teacher_id).first()
            
            if not validation.card_id_valid(
                    request, title, content, due_date,
                    discipline, teacher, status):
                return redirect('/client/admin/')

            add_card_person(
                request.user, title, content, due_date,
                discipline, teacher, status)
            messages.success(request, 'Card criado com sucesso.')
            messages.success(request, 'Card adicionado a todos os alunos.')
            return redirect('/client/admin')
        except:
            messages.error(request, 'Erro interno do sistema.')
            return redirect('/client/admin')


@login_required(login_url='/auth/login/')
def client(request, pk):
    person = Person.objects.filter(id=pk).first()
    user = Person.objects.filter(user=request.user).first()

    if not person.id == user.id:
        messages.error(request, 'Você não tem permissão de acessar está página.')
        return redirect('/')

    if request.method == 'GET':       
        disciplines = Discipline.objects.all()
        teachers = Teacher.objects.all()
        status = ItemList.STATUS

        return render(request, 'pages/client.html',
                      context={
                          'person': person,
                          'disciplines': disciplines,
                          'teachers': teachers,
                          'status': status})

    elif request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        due_date = request.POST.get('due-date')
        discipline_id = request.POST.get('discipline')
        teacher_id = request.POST.get('teacher')
        status = request.POST.get('status')

        try:
            discipline = Discipline.objects.filter(id=discipline_id).first()
            teacher = Teacher.objects.filter(id=teacher_id).first()

            if not validation.card_id_valid(
                    request, title,
                    content, due_date,
                    discipline, teacher, status):
                return redirect(f'/client/{person.id}/')

            item_list = ItemList.objects.create(
                author=request.user,
                title=title,
                content=content,
                due_date=due_date,
                discipline=discipline,
                teacher=teacher,
                status=status,
                type='P'
            )
            item_list.save()
            person.item_list.add(item_list)
            messages.success(request, 'Card criado com sucesso.')
            return redirect('/client/admin')
        except:
            messages.error(request, 'Erro interno do sistema.')
            return redirect('/client/admin')


def add_card_person(
        author, title, content, due_date,
        discipline, teacher, status, type='A'):
    people = Person.objects.filter(level='AL')
    people = people.union(Person.objects.filter(level='AD'))
    for person in people:
        item_list = ItemList.objects.create(
            author=author,
            title=title,
            content=content,
            due_date=due_date,
            discipline=discipline,
            teacher=teacher,
            status=status,
            type=type
        )
        item_list.save()
        person.item_list.add(item_list)


@login_required(login_url='/auth/login')
def cards(request, pk):
    if request.method == 'GET':
        person = Person.objects.filter(id=pk).first()
        user = Person.objects.filter(user=request.user).first()

        if not user.id == person.id:
            messages.error(request, 'Você não tem permisão de acessar está página.')
            return redirect('/')

        person = Person.objects.get(user=request.user)
        atual_date = datetime.today().strftime("%Y-%m-%d")
        item_list_todo = person.item_list.filter(status='TODO').order_by('due_date')
        item_list_doing = person.item_list.filter(status='DOING').order_by('-due_date')
        item_list_done = person.item_list.filter(status='DONE').order_by('-due_date')

        return render(request, 'pages/cards.html', context={
            'atual_date': atual_date,
            'item_list_todo': item_list_todo,
            'item_list_done': item_list_done,
            'item_list_doing': item_list_doing,
            'person': person,
        })


@login_required(login_url='/auth/login')
def delete_card(request, pk_card, pk_person):
    if request.method == 'GET':
        person = Person.objects.filter(id=pk_person).first()
        user = Person.objects.filter(user=request.user).first()
        if not user.id == person.id:
            messages.error(request, 'Você não tem permissão.')
            return  redirect('/')

        card = ItemList.objects.filter(id=pk_card).first()
        card.delete()
        messages.success(request, 'Card deletado com sucesso.')
        return redirect(f'/client/cards/{person.id}')
    

@login_required(login_url='/auth/login')
def update_card(request, pk_card, pk_person):
    person = Person.objects.filter(id=pk_person).first()
    user = Person.objects.filter(user=request.user).first()
    card = ItemList.objects.filter(id=pk_card).first()

    if not user.id == person.id:
        messages.error(request, 'Você não tem permissão.')
        return  redirect('/')

    if request.method == 'GET':
        disciplines = Discipline.objects.all()
        teachers = Teacher.objects.all()

        return render(request, 'pages/update_card.html', context={
            'card': card,
            'person': person,
            'disciplines': disciplines,
            'teachers': teachers,
        })

    elif request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        due_date = request.POST.get('due-date')
        discipline_id = request.POST.get('discipline')
        teacher_id = request.POST.get('teacher')
        status = request.POST.get('status')

        try:
            discipline = Discipline.objects.get(id=discipline_id)
            teacher = Teacher.objects.get(id=teacher_id)

            if not validation.card_id_valid(request, title, content, due_date, discipline, teacher, status):
                return redirect(f'/client/update_card/{card.id}/{person.id}/')

            card.title = title
            card.content = content
            card.due_date = due_date
            card.discipline = discipline
            card.teacher = teacher
            card.status = status
            card.save()
            messages.success(request, 'Tarefa atualizada com sucesso.')
            return redirect(f'/client/cards/{person.id}/')
        except:
            messages.error(request, 'Erro interno no sistema.')
            return redirect(f'/client/update_card/{card.id}/{person.id}/')
        
