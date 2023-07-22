import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse

from . import token_generate


def send_email(path_template: str, subject: str, to: list, **kwargs) -> dict:
    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, to
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
    return {'status': 1}


def send_verify_user(request, user):
    # Gerar o token
    token = token_generate.vigenere_encrypt(
        user.email, os.environ.get('KEY_TOKEN')
    )

    # Enviar o email
    path_template = os.path.join(
        settings.BASE_DIR,
        (
            'apps/authentication/templates/'
            'emails/confirm_registration.html'
        )
    )
    url = request.get_host() + reverse(
        'auth:activate_account', kwargs={'token': token}
    )
    send_email(
        path_template, 'Cadastro confirmado', [user.email, ],
        username=user.username, link_ativacao=url
    )
