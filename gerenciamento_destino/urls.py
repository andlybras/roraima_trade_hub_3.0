from django.urls import path
from . import views

app_name = 'destino'

urlpatterns = [
    path('', views.pagina_inicial_destino, name='pagina_inicial'),
]