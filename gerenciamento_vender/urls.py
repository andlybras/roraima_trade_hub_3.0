# gerenciamento_vender/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm # <--- ADICIONE ESTA LINHA

app_name = 'vender'

urlpatterns = [
    # URLs da parte pública e do FAQ
    path('', views.pagina_inicial_vender, name='pagina_inicial'),
    path('perguntas-frequentes/', views.faq_view, name='faq'),
    path('perguntas-frequentes/submeter/', views.submeter_pergunta_view, name='submeter_pergunta'),
    path('minha-pergunta/<uuid:identificador>/', views.ver_resposta_view, name='ver_resposta'),
    path('pergunta-enviada-com-sucesso/', views.submissao_sucesso_view, name='submissao_sucesso'),
    
    # URLs de Cadastro e Ativação
    path('criar-perfil-empresarial/', views.criar_perfil_empresarial_view, name='criar_perfil_empresarial'),
    path('cadastro-realizado/', views.cadastro_sucesso_view, name='cadastro_sucesso'),
    path('ativar/<uidb64>/<token>/', views.ativar_conta_view, name='ativar_conta'),
    
    # URLs de Autenticação
    path('acessar/', auth_views.LoginView.as_view(
        template_name='gerenciamento_vender/html/login.html',
        authentication_form=UserLoginForm,
        redirect_authenticated_user=True
    ), name='login'),
    path('sair/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # URL principal do Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # URLS para as abas do Dashboard
    path('dashboard/visao-geral/', views.dashboard_visao_geral, name='dashboard_visao_geral'),
    path('dashboard/dados-empresariais/', views.dashboard_dados_empresariais, name='dashboard_dados_empresariais'),
    path('dashboard/dados-empresariais/etapa/<int:etapa>/', views.dados_empresariais_form_view, name='dados_empresariais_form'),
     path('recuperar-senha/', auth_views.PasswordResetView.as_view(
        template_name='gerenciamento_vender/html/password_reset_form.html',
        email_template_name='gerenciamento_vender/html/emails/password_reset_email.html',
        subject_template_name='gerenciamento_vender/html/emails/password_reset_subject.txt',
        success_url='/quero-vender/recuperar-senha/email-enviado/'
    ), name='password_reset'),

    path('recuperar-senha/email-enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='gerenciamento_vender/html/password_reset_done.html'
    ), name='password_reset_done'),

    path('recuperar-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='gerenciamento_vender/html/password_reset_confirm.html',
        success_url='/quero-vender/recuperar-senha/sucesso/'
    ), name='password_reset_confirm'),

    path('recuperar-senha/sucesso/', auth_views.PasswordResetCompleteView.as_view(
        template_name='gerenciamento_vender/html/password_reset_complete.html'
    ), name='password_reset_complete'),
]