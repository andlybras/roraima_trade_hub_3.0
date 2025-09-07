# Arquivo: gerenciamento_inteligencia_mercado/urls.py
from django.urls import path
from . import views

app_name = 'inteligencia'

urlpatterns = [
    # Ex: /inteligencia-de-mercado/
    path('', views.pagina_inicial_inteligencia, name='pagina_inicial'),
    
    # ROTA ESPECÍFICA VEM PRIMEIRO
    path('glossario/', views.glossario_view, name='glossario'),
    
    # ROTA DO CONTEÚDO VEM DEPOIS DA DO GLOSSÁRIO
    path('conteudo/<int:pk>/', views.detalhe_conteudo, name='detalhe_conteudo'),

    # ROTA GENÉRICA VEM POR ÚLTIMO
    path('<str:categoria>/', views.lista_conteudo_por_categoria, name='lista_por_categoria'),
    path('grafico/preview/<int:pk>/', views.grafico_preview_view, name='grafico_preview'),
]