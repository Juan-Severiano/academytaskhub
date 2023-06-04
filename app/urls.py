from django.urls import path
from .views import home, to_do

urlpatterns = [
    path('', home, name='home'),
    path('to_do/', to_do, name='to_do')
]
