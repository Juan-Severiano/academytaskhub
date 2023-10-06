import os

from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User

from utils import token_generate


def activate_account(request, token):
    email = token_generate.vigenere_decrypt(
        token, os.environ.get('KEY_TOKEN')
    )
    user = User.objects.filter(email=email).first()

    if user is not None:
        if user.is_active:
            messages.warning(request, 'Usuário já está ativo.')
            return redirect(reverse('auth:login'))

        user.is_active = True
        user.save()
        messages.success(request, 'Usuário ativo com sucesso.')
        return redirect(reverse('auth:login'))

    messages.error(request, 'Codigo inválido.')
    return redirect(reverse('home:home'))
