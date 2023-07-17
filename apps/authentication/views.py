from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from apps.client.models import Person, ItemList
from django.contrib import messages
from apps.validation import validation
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            message = 'Não pode acessar está pagina estando logado.'
            messages.error(request, message)
            return redirect(reverse('home:home'))

        data = request.session.get('register_form_data', None)

        return render(request, 'pages/register.html', {'data': data})
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        POST = request.POST.copy()
        POST.pop('password', None)
        POST.pop('confirm-password', None)
        request.session['register_form_data'] = POST

        if not validation.register_is_valid(
            request, username, email, password, confirm_password
        ):
            return redirect(reverse('auth:register'))

        try:
            user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password)
            user.save()
            person = Person.objects.create(user=user, level='AL')
            person.save()

            item_list = ItemList.objects.filter(type='A', root=True) \
                .select_related('author', 'discipline', 'teacher')

            for item in item_list:
                item_copy = copy_card(item)
                person.item_list.add(item_copy)

            messages.success(request, 'Registro realizado com sucesso.')
            del (request.session['register_form_data'])
            return redirect(reverse('auth:login'))
        except Exception as e:
            messages.error(request, f'Erro interno no sistema: {str(e)}')
            return redirect(reverse('auth:register'))
    else:
        messages.error(request, 'Requisição inválida.')
        return redirect(reverse('auth:register'))


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


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            message = 'Não pode acessar está pagina estando logado.'
            messages.error(request, message)
            return redirect(reverse('home:home'))

        data = request.session.get('login_form_data', None)
        return render(request, 'pages/login.html', {'data': data})
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        POST = request.POST.copy()
        POST.pop('password', None)
        request.session['login_form_data'] = POST

        if not validation.login_is_valid(request, email, password):
            return redirect(reverse('auth:login'))

        try:
            username = User.objects.filter(email=email).first()
            user = auth.authenticate(
                request, username=username, password=password
            )
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Usuário logou com sucesso.')
                del (request.session['login_form_data'])
                return redirect(reverse('home:home'))
            else:
                message = 'Não foi possível logar. Tente novamente.'
                messages.error(request, message)
                return redirect(reverse('auth:login'))
        except Exception as e:
            messages.error(request, f'Erro interno do sistema: {str(e)}')
            return redirect(reverse('auth:login'))
    else:
        messages.error(request, 'Requisição inválida.')
        return redirect(reverse('auth:login'))


@login_required(login_url='/auth/login/', redirect_field_name='next')
def logout(request):
    if not request.POST:
        messages.error(request, 'Requisição de logout inválida.')
        return redirect(reverse('home:home'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'User logout inválido.')
        return redirect(reverse('home:home'))

    auth.logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect(reverse('auth:login'))
