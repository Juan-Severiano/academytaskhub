from django.urls import path
from . import views


app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('status/<str:status>/', views.specific_status,
         name='specific_status'),
    path('terms/', views.terms, name='terms'),
]
