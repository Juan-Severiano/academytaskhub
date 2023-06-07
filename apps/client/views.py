from django.shortcuts import render, redirect
from django.contrib import messages
from apps.client.models import Person, Discipline, Teacher, ItemList
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User


@login_required(login_url='/auth/login')
def admin(request):
    if request.method == 'GET':
        person = Person.objects.get(user=request.user)
        if not person.level == 'AD':
            messages.error(request, 'Você não tem permissão de acessar está página.')
            return redirect('/')
        
        disciplines = Discipline.objects.all()
        teachers = Teacher.objects.all()

        return render(request, 'pages/admin.html', context={'disciplines': disciplines, 'teachers': teachers})
    elif request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        due_date = request.POST.get('due-date')
        discipline = request.POST.get('discipline')
        teacher = request.POST.get('teacher')

        try:
            discipline = Discipline.objects.filter(id=discipline).first()
            teacher = Teacher.objects.filter(id=teacher).first()
            item_list = ItemList.objects.create(
                author = request.user,
                title = title,
                content = content,
                due_date = due_date,
                discipline = discipline,
                teacher = teacher,
                status = 'TODO',
                type = 'A'
            )
            item_list.save()
            messages.success(request, 'Card criado com sucesso.')
            
            add_card_person(item_list)
            messages.success(request, 'Card adicionado a todos os alunos.')

            return redirect('/client/admin')
        except:
            messages.error(request, 'Erro interno do sistema.')
            return redirect('/client/admin')
        
def add_card_person(item_list):
    people = Person.objects.filter(level='AL')
    people = people.union(Person.objects.filter(level='AD'))
    for person in people:
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
        item_list_doing = person.item_list.filter(due_date=atual_date).filter(status='DOING').order_by('-due_date')
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
    
    
# @login_required(login_url='/auth/login')
# def update_card(request, pk_card, pk_person):
#     if request.method == 'GET':
#         person = Person.objects.filter(id=pk_person).first()
#         user = Person.objects.filter(user=request.user).first()
#         if not user.id == person.id:
#             messages.error(request, 'Você não tem permissão.')
#             return  redirect('/')
        
#         card = ItemList.objects.filter(id=pk_card).first()
#         disciplines = Discipline.objects.all()
#         teachers = Teacher.objects.all()
#         return render(request, 'pages/update_card.html', context={
#             card: card,
#             disciplines: disciplines,
#             teachers: teachers,
#             person: person
#         })

        
