from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from apps.client.models import Person
from django.contrib import messages
from apps.validation import validation
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.error(request, 'Não pode acessar está pagina estando logado')
            return redirect('/')
        return render(request, 'pages/register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if not validation.register_is_valid(request, username, email, password, confirm_password):
            return redirect('/auth/register')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            person = Person.objects.create(user=user, level='AL')
            person.save()
            messages.success(request, 'Registro realizado com sucesso.')
            return redirect('/auth/login')
        except:
            messages.erro(request, 'Erro interno no sistema.')
            return redirect('/auth/register')

def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.error(request, 'Não pode acessar está pagina estando logado')
            return redirect('/')
        return render(request, 'pages/login.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not validation.login_is_valid(request, email, password):
            return redirect('/auth/login')
        
        try:
            username = User.objects.filter(email=email).first()
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Usuário logocou com sucesso')
                return redirect('/')
            else:
                messages.error(request, 'Não foi possível logar. Tente novamente.')
                return redirect('/auth/login')
        except:
            messages.error(request, 'Erro interno do sistema.')
            return redirect('/auth/login')

@login_required(login_url='/auth/login')
def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        messages.success(request, 'Usuário deslogou com sucesso')
        return redirect('/auth/login')