from django.contrib.auth.models import User

from rest_framework import serializers

from apps.client.models import Person, ItemList
from apps.validation import validation_rest
from utils import card_generate, email_generate


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

        email_generate.send_verify_user(self.context.get('request'), user)

        person = Person.objects.create(user=user, level='AL')
        person.save()

        item_list = ItemList.objects.filter(type='A', root=True) \
            .select_related('author', 'discipline', 'teacher')

        for item in item_list:
            item_copy = card_generate.copy_card(item)
            person.item_list.add(item_copy)

        return user
