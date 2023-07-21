from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.routers import SimpleRouter
from . import views

from .permissions import IsActiveUserPermission


author_api_router = SimpleRouter()
author_api_router.register('api/user', views.UserViewSets, basename='user-api')


app_name = 'auth'


class TokenObtainPairViewIsActive(TokenObtainPairView):
    permission_classes = [IsActiveUserPermission]


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate_account/<str:token>/', views.activate_account,
         name='activate_account'),
    path('api/token/', TokenObtainPairViewIsActive.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(),
         name='token_verify'),
]

urlpatterns += author_api_router.urls
