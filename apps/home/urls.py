from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('to_do/', views.to_do, name='to_do'),
    path('doing/', views.doing, name='doing'),
    path('done/', views.done, name='done'),
]
