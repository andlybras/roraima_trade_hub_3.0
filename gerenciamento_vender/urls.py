# gerenciamento_vender/urls.py

from django.urls import path
from . import views

app_name = 'vender'

urlpatterns = [
    # URLs existentes
    path('', views.pagina_inicial_vender, name='pagina_inicial'),
    path('perguntas-frequentes/', views.faq_view, name='faq'),
    path('perguntas-frequentes/submeter/', views.submeter_pergunta_view, name='submeter_pergunta'),
    path('minha-pergunta/<uuid:identificador>/', views.ver_resposta_view, name='ver_resposta'),
    path('pergunta-enviada-com-sucesso/', views.submissao_sucesso_view, name='submissao_sucesso'),
    path('criar-perfil-empresarial/', views.criar_perfil_empresarial_view, name='criar_perfil_empresarial'),
    
    # URL DO DASHBOARD PRINCIPAL
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # URLS PARA CADA ABA DO DASHBOARD (PARA O AJAX)
    path('dashboard/visao-geral/', views.dashboard_visao_geral, name='dashboard_visao_geral'),
    path('dashboard/dados-empresariais/', views.dashboard_dados_empresariais, name='dashboard_dados_empresariais'),
    # Adicionaremos as outras conforme formos construindo...
]