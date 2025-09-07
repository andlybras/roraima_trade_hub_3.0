# Arquivo: gerenciamento_inteligencia_mercado/urls.py
from django.urls import path
from . import views

app_name = 'inteligencia'

urlpatterns = [
    # Ex: /inteligencia-de-mercado/
    path('', views.pagina_inicial_inteligencia, name='pagina_inicial'),

    # Ex: /inteligencia-de-mercado/dados-estruturais/
    path('<str:categoria>/', views.lista_conteudo_por_categoria, name='lista_por_categoria'),
    path('conteudo/<int:pk>/', views.detalhe_conteudo, name='detalhe_conteudo'),
]