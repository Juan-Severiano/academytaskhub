import re

from collections import defaultdict

from django.contrib.auth.models import User

from rest_framework import serializers

from apps.client.models import ItemList


def username_is_valid(
        username: str, errors: dict, verify_exist: bool = True
) -> dict:
    if len(username.strip()) <= 0:
        errors['username'].append('Prencha o campo de username.')

    if verify_exist:
        username_exist = User.objects.filter(username=username).exists()
        if username_exist:
            errors['username'].append('Username já utilizado.')

    return errors


def email_is_valid(
        email: str, errors: dict, verify_exist: bool = True,
) -> dict:
    # exemple@@aluno.ce.gov.br
    email_pattern = r'^[a-zA-Z0-9._%+-]+@aluno\.ce\.gov\.br$'

    if len(email.strip()) <= 0:
        errors['email'].append('Prencha o campo de email.')

    if not re.match(email_pattern, email):
        errors['email'].append('O email precisa ser do gov.br.')

    if verify_exist:
        email_exist = User.objects.filter(email=email).exists()
        if email_exist:
            errors['email'].append('Email já utilizado.')

    return errors


def password_is_valid(
        password: str, confirm_password: str = '',
        errors: dict = {}, verify_passwords: bool = True
) -> dict:
    if len(password.strip()) <= 0:
        errors['password'].append('Prencha o campo de senha.')

    if verify_passwords:
        if len(confirm_password.strip()) <= 0:
            errors['confirm_password'].append(
                'Prencha o campo de confirmar senha.'
            )

        if password != confirm_password:
            errors['password'].append('As senhas não coicidem.')
            errors['confirm_password'].append('As senhas não coicidem.')

    return errors


def register_is_valid(
        username: str, email: str,
        password: str, confirm_password: str,
) -> dict:
    errors = defaultdict(list)
    username_is_valid(username, errors)
    email_is_valid(email, errors)
    password_is_valid(password, confirm_password, errors)

    if errors:
        raise serializers.ValidationError(errors)


def update_is_valid(
        username: str, email: str,
        password: str, confirm_password: str,
) -> dict:
    errors = defaultdict(list)
    username_is_valid(username, errors, verify_exist=False)
    email_is_valid(email, errors, verify_exist=False)
    password_is_valid(password, confirm_password, errors)

    if errors:
        raise serializers.ValidationError(errors)


def login_is_valid(request: any, email: str, password: str) -> bool:
    if not email_is_valid(request, email, verify_exist=False):
        return False
    if not password_is_valid(request, password, verify_passwords=False):
        return False
    return True


def card_id_valid(
        title: str, content: str, due_date: str,
        discipline: object, teacher: object, status: object
) -> bool:
    if len(title.strip()) <= 0:
        serializers.ValidationError('Prencha o campo de titulo.')
        return False

    if len(content.strip()) <= 0:
        serializers.ValidationError('Prencha o campo de conteudo.')
        return False

    if len(due_date.strip()) <= 0:
        serializers.ValidationError('Prencha o campo de data.')
        return False

    if discipline is None:
        serializers.ValidationError('Selecione uma disciplina.')
        return False

    if teacher is None:
        serializers.ValidationError('Selecione um professor.')
        return False

    STATUS = [item[0] for item in ItemList.STATUS]
    if (status is None) or (status not in STATUS):
        serializers.ValidationError('Seleceione o estado da tarefa.')
        return False

    return True
