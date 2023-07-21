import os

from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import serializers

from apps.client.models import Person, ItemList
from apps.validation import validation_rest

from utils import token_generate, email_generate


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password']

    def validate(self, attrs):
        validation_rest.register_is_valid(
            attrs.get('username', ''), attrs.get('email', ''),
            attrs.get('password', ''), attrs.get('confirm_password', '')
        )
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data, is_active=False)
        user.save()

        send_verify_user(self.context.get('request'), user)

        person = Person.objects.create(user=user, level='AL')
        person.save()

        item_list = ItemList.objects.filter(type='A', root=True) \
            .select_related('author', 'discipline', 'teacher')

        for item in item_list:
            item_copy = copy_card(item)
            person.item_list.add(item_copy)

        return user


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
    email_generate.send_email(
        path_template, 'Cadastro confirmado', [user.email, ],
        username=user.username, link_ativacao=url
    )
