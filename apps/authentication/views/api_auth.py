from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework_simplejwt.views import TokenObtainPairView

from .. import serializers
from apps.authentication.permissions import IsOwner, IsActiveUserPermission


class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    http_method_names = ['get', 'options', 'head', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request"] = self.request
        return context


class TokenObtainPairViewIsActive(TokenObtainPairView):
    permission_classes = [IsActiveUserPermission]
