from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework_simplejwt.views import TokenObtainPairView

from .. import serializers
from apps.authentication.permissions import IsOwner, IsActiveUserPermission


class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    http_method_names = ['get', 'options', 'head', 'post']

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj)
        self.permission_classes.clear()
        self.permission_classes += [IsAuthenticated, IsOwner]
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        return super().create(
            request, *args, **kwargs, context={'request': request}
        )


class TokenObtainPairViewIsActive(TokenObtainPairView):
    permission_classes = [IsActiveUserPermission]
