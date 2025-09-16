# gerenciamento_vender/urls.py

from django.urls import path
from . import views

app_name = 'vender'

urlpatterns = [
    path('', views.pagina_inicial_vender, name='pagina_inicial'),
    path('perguntas-frequentes/', views.faq_view, name='faq'),
    
    # NOVAS URLs ADICIONADAS:
    path('perguntas-frequentes/submeter/', views.submeter_pergunta_view, name='submeter_pergunta'),
    path('minha-pergunta/<uuid:identificador>/', views.ver_resposta_view, name='ver_resposta'),
    path('pergunta-enviada-com-sucesso/', views.submissao_sucesso_view, name='submissao_sucesso'),

    # URLs existentes
    path('criar-perfil-empresarial/', views.criar_perfil_empresarial_view, name='criar_perfil_empresarial'),
    path('acessar-ambiente-empresarial/', views.acessar_ambiente_empresarial_view, name='acessar_ambiente_empresarial'),
]