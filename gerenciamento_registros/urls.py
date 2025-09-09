from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import (
    EmpresaEmpreendedorRegisterView, 
    AprendizRegisterView, 
    activate, 
    resend_activation_email_view,
    perfil_update_view
)
from .forms import PublicAuthenticationForm

app_name = 'gerenciamento_registros'

urlpatterns = [
    path('registro/empresa-empreendedor/', EmpresaEmpreendedorRegisterView.as_view(), name='registro_empresa_empreendedor'),
    path('registro/aprendiz/', AprendizRegisterView.as_view(), name='registro_aprendiz'),
    path('ativacao-enviada/', TemplateView.as_view(template_name='gerenciamento_registros/html/ativacao_enviada.html'), name='ativacao_enviada'),
    path('ativar/<str:uidb64>/<str:token>/', activate, name='ativar_conta'),
    path('ativacao/sucesso/', TemplateView.as_view(template_name='gerenciamento_registros/html/ativacao_sucesso.html'), name='ativacao_sucesso'),
    path('ativacao/invalida/', TemplateView.as_view(template_name='gerenciamento_registros/html/ativacao_invalida.html'), name='ativacao_invalida'),
    path('login/', auth_views.LoginView.as_view(template_name='gerenciamento_registros/html/login.html', redirect_authenticated_user=True, authentication_form=PublicAuthenticationForm), name='login'),
    path('reenviar-ativacao/', resend_activation_email_view, name='resend_activation'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('perfil/', perfil_update_view, name='perfil_update'),
    path('recuperar-senha/', auth_views.PasswordResetView.as_view(
        template_name='gerenciamento_registros/html/password_reset_form.html',
        email_template_name='gerenciamento_registros/emails/password_reset_email.html',
        subject_template_name='gerenciamento_registros/emails/password_reset_subject.txt',
        success_url='/contas/recuperar-senha/enviado/'
    ), name='password_reset'),
    path('recuperar-senha/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='gerenciamento_registros/html/password_reset_done.html'
    ), name='password_reset_done'),
    path('recuperar-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='gerenciamento_registros/html/password_reset_confirm.html',
        success_url='/contas/recuperar-senha/sucesso/'
    ), name='password_reset_confirm'),
    path('recuperar-senha/sucesso/', auth_views.PasswordResetCompleteView.as_view(
        template_name='gerenciamento_registros/html/password_reset_complete.html'
    ), name='password_reset_complete'),
]