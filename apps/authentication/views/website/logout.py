from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required


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
