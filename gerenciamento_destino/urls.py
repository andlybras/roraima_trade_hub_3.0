# gerenciamento_destino/urls.py

from django.urls import path
from . import views

app_name = 'destino'

urlpatterns = [
    path('', views.pagina_inicial_destino, name='pagina_inicial'),
    path('mapa/<slug:categoria_slug>/', views.mapa_categoria_view, name='mapa_categoria'),
    
    # NOVA ROTA para a página de detalhes de um ponto específico
    path('ponto/<slug:ponto_slug>/', views.detalhe_ponto_view, name='detalhe_ponto'),
]