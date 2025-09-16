# gerenciamento_vender/urls.py

from django.urls import path
from . import views

app_name = 'vender'

urlpatterns = [
    # URLs da parte pública e do FAQ (continuam as mesmas)
    path('', views.pagina_inicial_vender, name='pagina_inicial'),
    path('perguntas-frequentes/', views.faq_view, name='faq'),
    path('perguntas-frequentes/submeter/', views.submeter_pergunta_view, name='submeter_pergunta'),
    path('minha-pergunta/<uuid:identificador>/', views.ver_resposta_view, name='ver_resposta'),
    path('pergunta-enviada-com-sucesso/', views.submissao_sucesso_view, name='submissao_sucesso'),
    path('criar-perfil-empresarial/', views.criar_perfil_empresarial_view, name='criar_perfil_empresarial'),
    
    # URL principal do Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # URLS para as abas do Dashboard (carregadas via AJAX)
    path('dashboard/visao-geral/', views.dashboard_visao_geral, name='dashboard_visao_geral'),
    
    # URL de "entrada" para os Dados Empresariais. É a que o link da navbar chama.
    path('dashboard/dados-empresariais/', views.dashboard_dados_empresariais, name='dashboard_dados_empresariais'),
    
    # NOVA URL que controla cada etapa do formulário. É para onde a view acima redireciona.
    path('dashboard/dados-empresariais/etapa/<int:etapa>/', views.dados_empresariais_form_view, name='dados_empresariais_form'),
]