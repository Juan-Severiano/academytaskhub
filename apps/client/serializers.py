from rest_framework import serializers

from .models import Teacher, Discipline, ItemList, Person
from apps.authentication.serializers import UserSerializer

from utils.card_generate import get_item_list


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name']


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ['id', 'name', 'is_technical_area']


class ItemListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    discipline = serializers.PrimaryKeyRelatedField(
        queryset=Discipline.objects.all(), required=True)
    teacher = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), required=True)
    type = serializers.CharField(default='P', max_length=1)

    class Meta:
        model = ItemList
        fields = [
            'id', 'author', 'title', 'content', 'due_date',
            'discipline', 'teacher', 'status', 'type'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if self.context['request'].user.is_staff:
            data['root'] = instance.root

        data['discipline'] = DisciplineSerializer(instance.discipline).data
        data['teacher'] = TeacherSerializer(instance.teacher).data

        return data


class ItemListAdminSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    discipline = serializers.PrimaryKeyRelatedField(
        queryset=Discipline.objects.all(), required=True)
    teacher = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), required=True)
    root = serializers.BooleanField(default=True)
    type = serializers.CharField(default='A', max_length=1)

    class Meta:
        model = ItemList
        fields = [
            'id', 'author', 'title', 'content', 'due_date',
            'discipline', 'teacher', 'status', 'type', 'root'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['discipline'] = DisciplineSerializer(instance.discipline).data
        data['teacher'] = TeacherSerializer(instance.teacher).data

        return data


class PersonSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    item_list = serializers.PrimaryKeyRelatedField(
        many=True, queryset=get_item_list(ItemList)
    )

    class Meta:
        model = Person
        fields = ['id', 'user', 'level', 'item_list']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['item_list'] = ItemListSerializer(
            instance.item_list, many=True,
            context={'request': self.context['request']}
        ).data

        return data
