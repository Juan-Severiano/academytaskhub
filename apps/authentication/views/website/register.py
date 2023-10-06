from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from apps.client.models import Person, ItemList
from utils import card_generate, email_generate
from apps.validation import validation


def register(request):
    if request.user.is_authenticated:
        messages.error(request, 'Não pode acessar está pagina estando logado.')
        return redirect(reverse('home:home'))

    if request.method == 'GET':
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
                    password=password,
                    is_active=False
                )
            user.save()

            email_generate.send_verify_user(request, user)

            person = Person.objects.create(user=user, level='AL')
            person.save()

            item_list = card_generate.get_item_list(ItemList, type='A', root=True)
            for item in item_list:
                item_copy = card_generate.copy_card(item)
                person.item_list.add(item_copy)

            message = (
                'Registro realizado com sucesso. Enviamos um email para você.'
            )
            messages.success(request, message)
            del (request.session['register_form_data'])
            return redirect(reverse('auth:login'))
        except Exception as e:
            messages.error(request, f'Erro interno no sistema: {str(e)}')
            return redirect(reverse('auth:register'))
    else:
        messages.error(request, 'Requisição inválida.')
        return redirect(reverse('auth:register'))
