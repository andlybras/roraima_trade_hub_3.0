from django.urls import path
from . import views

app_name = 'aprenda'

urlpatterns = [
    path('', views.pagina_inicial_aprenda, name='pagina_inicial'),
]