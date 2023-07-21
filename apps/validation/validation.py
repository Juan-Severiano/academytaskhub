from django.contrib import messages
from django.contrib.auth.models import User
from apps.client.models import ItemList
import re


def username_is_valid(request: any, username: str) -> bool:
    if len(username.strip()) <= 0:
        messages.error(request, 'Prencha o campo de username.')
        return False

    username_exist = User.objects.filter(username=username).exists()
    if username_exist:
        messages.error(request, 'Username já utilizado.')
        return False

    return True


def email_is_valid(
        request: any, email: str, verify_exist: bool = True
) -> bool:
    email_pattern = r'^[a-zA-Z0-9._%+-]+@aluno\.ce\.gov\.br$'

    if len(email.strip()) <= 0:
        messages.error(request, 'Prencha o campo de email.')
        return False

    if not re.match(email_pattern, email):
        messages.error(request, 'O email precisa ser do gov.br.')
        return False

    if verify_exist:
        email_exist = User.objects.filter(email=email).exists()
        if email_exist:
            messages.error(request, 'Email já utilizado.')
            return False

    return True


def password_is_valid(
        request: any, password: str, confirm_password: str = '',
        verify_passwords: bool = True
) -> bool:
    if len(password.strip()) <= 0:
        messages.error(request, 'Prencha o campo de senha.')
        return False

    if verify_passwords:
        if len(confirm_password.strip()) <= 0:
            messages.error(request, 'Prencha o campo de confirmar senha.')
            return False

        if password != confirm_password:
            messages.error(request, 'As senhas não coicidem.')
            return False

    return True


def register_is_valid(
        request: any, username: str, email: str,
        password: str, confirm_password: str,
) -> bool:
    if not username_is_valid(request, username):
        return False
    if not email_is_valid(request, email):
        return False
    if not password_is_valid(request, password, confirm_password):
        return False
    return True


def login_is_valid(request: any, email: str, password: str) -> bool:
    if not email_is_valid(request, email, verify_exist=False):
        return False
    if not password_is_valid(request, password, verify_passwords=False):
        return False
    return True


def card_id_valid(
        request: any, title: str, content: str, due_date: str,
        discipline: object, teacher: object, status: object
) -> bool:
    if len(title.strip()) <= 0:
        messages.error(request, 'Prencha o campo de titulo.')
        return False

    if len(content.strip()) <= 0:
        messages.error(request, 'Prencha o campo de conteudo.')
        return False

    if len(due_date.strip()) <= 0:
        messages.error(request, 'Prencha o campo de data.')
        return False

    if discipline is None:
        messages.error(request, 'Selecione uma disciplina.')
        return False

    if teacher is None:
        messages.error(request, 'Selecione um professor.')
        return False

    STATUS = [item[0] for item in ItemList.STATUS]
    if (status is None) or (status not in STATUS):
        messages.error(request, 'Seleceione o estado da tarefa.')
        return False

    return True
