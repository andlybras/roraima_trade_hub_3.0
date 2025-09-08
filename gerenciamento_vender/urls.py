# Arquivo: gerenciamento_vendas/urls.py

from django.urls import path
from . import views

app_name = 'vender'

urlpatterns = [
    path('', views.pagina_inicial_vender, name='pagina_inicial'),
]