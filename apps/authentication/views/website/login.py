from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User

from utils import email_generate
from apps.validation import validation


def login(request):
    if request.user.is_authenticated:
        messages.error(request, 'Não pode acessar está pagina estando logado.')
        return redirect(reverse('home:home'))

    if request.method == 'GET':
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
                if not username.is_active:
                    message = (
                        'Você ainda não ativou sua conta no email. '
                        'Acabamos de lhe enviar outro'
                    )
                    messages.error(request, message)
                    email_generate.send_verify_user(request, username)
                    return redirect(reverse('auth:login'))

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
