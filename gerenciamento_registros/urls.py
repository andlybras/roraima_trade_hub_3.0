from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import EmpresaEmpreendedorRegisterView, AprendizRegisterView, activate
from .forms import PublicAuthenticationForm

app_name = 'gerenciamento_registros'

urlpatterns = [
    path('registro/empresa-empreendedor/', EmpresaEmpreendedorRegisterView.as_view(), name='registro_empresa_empreendedor'),
    path('registro/aprendiz/', AprendizRegisterView.as_view(), name='registro_aprendiz'),
    path('ativacao-enviada/', TemplateView.as_view(template_name='gerenciamento_registros/html/ativacao_enviada.html'), name='ativacao_enviada'),
    path('ativar/<str:uidb64>/<str:token>/', activate, name='ativar_conta'),
    path('ativacao/sucesso/', TemplateView.as_view(template_name='gerenciamento_registros/html/ativacao_sucesso.html'), name='ativacao_sucesso'),
    path('ativacao/invalida/', TemplateView.as_view(template_name='gerenciamento_registros/html/ativacao_invalida.html'), name='ativacao_invalida'),
    path('login/', auth_views.LoginView.as_view(
        template_name='gerenciamento_registros/html/login.html',
        redirect_authenticated_user=True,
        authentication_form=PublicAuthenticationForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/' 
    ), name='logout'),
]