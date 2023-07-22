from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from rest_framework.routers import SimpleRouter
from . import views


app_name = 'auth'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate_account/<str:token>/', views.activate_account,
         name='activate_account'),
]


urlpatterns_jwt = [
    path('api/token/', views.TokenObtainPairViewIsActive.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(),
         name='token_verify'),
]


# Django Rest Framework
auth_api_router = SimpleRouter()
auth_api_router.register('api/user', views.UserViewSets, basename='user-api')


urlpatterns += urlpatterns_jwt
urlpatterns += auth_api_router.urls
