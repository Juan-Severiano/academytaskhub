from django.urls import path
from . import views


app_name = 'client'

urlpatterns = [
    path('<int:pk>/', views.client, name='client'),
    path('admin/', views.admin, name='admin'),
    path('cards/<int:pk>/', views.cards, name='cards'),
    path('delete_card/<int:pk_card>/<int:pk_person>/',
         views.delete_card, name='delete_card'),
    path('update_card/<int:pk_card>/<int:pk_person>/',
         views.update_card, name='update_card'),
]
