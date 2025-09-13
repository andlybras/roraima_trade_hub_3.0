# gerenciamento_destino/urls.py

from django.urls import path
from . import views

app_name = 'destino'

urlpatterns = [
    path('', views.pagina_inicial_destino, name='pagina_inicial'),
    path('belezas-da-natureza/', views.belezas_da_natureza_view, name='belezas_da_natureza'),
    path('cultura-e-tradicoes/', views.cultura_e_tradicoes_view, name='cultura_e_tradicoes'),
    # A URL de serviços foi completamente removida
    path('ponto/<slug:ponto_slug>/', views.detalhe_ponto_view, name='detalhe_ponto'),
]