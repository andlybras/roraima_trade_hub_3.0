from django.urls import path
from . import views

app_name = 'destino'

urlpatterns = [
    path('', views.pagina_inicial_destino, name='pagina_inicial'),
    path('belezas-da-natureza/', views.belezas_da_natureza_view, name='belezas_da_natureza'),
    path('cultura-e-tradicoes/', views.cultura_e_tradicoes_view, name='cultura_e_tradicoes'),
    path('ponto/<slug:ponto_slug>/', views.detalhe_ponto_view, name='detalhe_ponto'),
    path('roteiros/', views.lista_roteiros_view, name='lista_roteiros'),
    path('roteiros/<slug:roteiro_slug>/', views.detalhe_roteiro_view, name='detalhe_roteiro'),
    path('meu-roteiro/', views.meu_roteiro_view, name='meu_roteiro'),
    path('api/dados-roteiro/', views.dados_roteiro_api_view, name='dados_roteiro_api'),
]