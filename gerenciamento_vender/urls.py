from django.urls import path
from . import views

app_name = 'vender'

urlpatterns = [
    # URLs da parte pública e do FAQ
    path('', views.pagina_inicial_vender, name='pagina_inicial'),
    path('perguntas-frequentes/', views.faq_view, name='faq'),
    path('perguntas-frequentes/submeter/', views.submeter_pergunta_view, name='submeter_pergunta'),
    path('minha-pergunta/<uuid:identificador>/', views.ver_resposta_view, name='ver_resposta'),
    path('pergunta-enviada-com-sucesso/', views.submissao_sucesso_view, name='submissao_sucesso'),
    
    # URL de Cadastro
    path('criar-perfil-empresarial/', views.criar_perfil_empresarial_view, name='criar_perfil_empresarial'),
    # CORREÇÃO AQUI: Apontando para a view correta.
    path('cadastro-realizado/', views.cadastro_sucesso_view, name='cadastro_sucesso'),
    
    # URL principal do Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # URLS para as abas do Dashboard
    path('dashboard/visao-geral/', views.dashboard_visao_geral, name='dashboard_visao_geral'),
    path('dashboard/dados-empresariais/', views.dashboard_dados_empresariais, name='dashboard_dados_empresariais'),
    path('dashboard/dados-empresariais/etapa/<int:etapa>/', views.dados_empresariais_form_view, name='dados_empresariais_form'),
]