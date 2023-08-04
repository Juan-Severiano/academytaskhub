from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.client.models import Person, ItemList
from apps.validation import validation_rest
from utils import card_generate, email_generate


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password',
            'confirm_password', 'is_active'
        ]

    def validate(self, attrs):
        request = self.context.get('request')
        instance = self.instance
        if request.method == 'POST':
            validation_rest.register_is_valid(
                attrs.get('username', ''), attrs.get('email', ''),
                attrs.get('password', ''), attrs.get('confirm_password', '')
            )
        elif request.method in ['PUT', 'PATCH']:
            validation_rest.update_is_valid(
                instance, attrs.get('email', ''),
                attrs.get('password', ''), attrs.get('confirm_password', '')
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data, is_active=False)
        user.save()

        email_generate.send_verify_user(self.context.get('request'), user)

        person = Person.objects.create(user=user, level='AL')
        person.save()

        item_list = ItemList.objects.filter(type='A', root=True) \
            .select_related('author', 'discipline', 'teacher')

        for item in item_list:
            item_copy = card_generate.copy_card(item)
            person.item_list.add(item_copy)

        return user

    def update(self, instance, validated_data):
        if instance.email != validated_data.get('email'):
            instance.is_active = False
            instance.email = validated_data.get('email')
            email_generate.send_verify_user(
                self.context.get('request'), instance
            )
        return super().update(instance, validated_data)


class TokenObtainPairViewIsActiveSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        request = self.context['request']
        is_email = request.query_params.get('email', None)

        if is_email == 'True':
            email = attrs.get('username', None)
            user = get_object_or_404(User, email=email)

            attrs['username'] = user.username
        return super().validate(attrs)
