from django.urls import path
from rest_framework.routers import SimpleRouter
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


# Django Rest Framework
client_api_router = SimpleRouter()
client_api_router.register(
    'api/teacher', views.TeacherViewSets, basename='teacher-api'
)
client_api_router.register(
    'api/discipline', views.DisciplineViewSets, basename='discipline-api'
)
client_api_router.register(
    'api/itemlist', views.ItemListViewSets, basename='itemlist-api'
)
client_api_router.register(
    'api/itemlist-admin', views.ItemListAdminViewSets,
    basename='itemlist-admin-api'
)
client_api_router.register(
    'api/person', views.PersonViewSets, basename='person-api'
)

urlpatterns += client_api_router.urls
