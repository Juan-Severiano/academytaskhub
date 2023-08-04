from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.serializers import ValidationError
from utils import email_generate


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj == request.user

    def has_permission(self, request, view):
        return super().has_permission(request, view)


class IsOwnerItemList(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.author == request.user

    def has_permission(self, request, view):
        return super().has_permission(request, view)


class IsOwnerPerson(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.user == request.user

    def has_permission(self, request, view):
        return super().has_permission(request, view)


class IsActiveUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        field = {'username': request.data.get('username')}
        if request.query_params.get('email'):
            field = {'email': request.data.get('username')}

        user = User.objects.filter(**field).first()
        if user is None:
            raise ValidationError({
                'detail': 'Usuário e/ou senha incorreto(s) dd'
            })
        if not user.is_active:
            message = (
                'Você ainda não ativou sua conta no email. '
                'Acabamos de lhe enviar outro email.'
            )
            email_generate.send_verify_user(request, user)
            raise ValidationError(message)

        return user.is_active
