from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .. import serializers
from .. import models
from apps.authentication.permissions import IsOwnerItemList, IsOwnerPerson

from utils.card_generate import get_item_list, add_card_person
from utils.person_generate import get_person_list, get_person


class TeacherViewSets(viewsets.ModelViewSet):
    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer

    def get_permissions(self):
        if self.request.method != 'GET':
            return [IsAdminUser()]
        return [IsAuthenticated()]


class DisciplineViewSets(viewsets.ModelViewSet):
    queryset = models.Discipline.objects.all()
    serializer_class = serializers.DisciplineSerializer

    def get_permissions(self):
        if self.request.method != 'GET':
            return [IsAdminUser()]
        return [IsAuthenticated()]


class ItemListViewSets(viewsets.ModelViewSet):
    queryset = get_item_list(models.ItemList)
    serializer_class = serializers.ItemListSerializer
    permission_classes = [IsAuthenticated, IsOwnerItemList]

    def list(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            self.queryset = get_item_list(
                models.ItemList, author=request.user
            )
        else:
            [IsAdminUser()]
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        person = get_person(user__id=self.request.user.id)
        person.item_list.add(serializer.instance)


class ItemListAdminViewSets(viewsets.ModelViewSet):
    queryset = get_item_list(models.ItemList)
    serializer_class = serializers.ItemListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        item_list = get_item_list(
            models.ItemList, author=self.request.user, root=False
        )
        item_list.delete()

        title = serializer.instance.title
        content = serializer.instance.content
        due_date = serializer.instance.due_date
        discipline = serializer.instance.discipline
        teacher = serializer.instance.teacher
        status = serializer.instance.status

        add_card_person(
            self.request.user, title, content,
            due_date, discipline, teacher, status
        )


class PersonViewSets(viewsets.ModelViewSet):
    queryset = get_person_list()
    serializer_class = serializers.PersonSerializer
    permission_classes = [IsAuthenticated, IsOwnerPerson]
    http_method_names = ['get', 'options', 'head']

    def list(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            self.queryset = get_person_list(user=self.request.user)
        else:
            [IsAdminUser()]
        return super().list(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(['get'], False)
    def me(self, request, *args, **kwargs):
        obj = get_person(user__id=request.user.id)
        serializers = self.get_serializer(
            instance=obj
        )
        return Response(serializers.data)
