from django.urls import path
from .views import home, to_do, doing, done, discipline


urlpatterns = [
    path('', home, name='home'),
    path('to_do/', to_do, name='to_do'),
    path('doing/', doing, name='doing'),
    path('done/', done, name='done'),
]
