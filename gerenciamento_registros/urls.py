# Arquivo: gerenciamento_registros/urls.py

from django.urls import path
from django.views.generic import TemplateView
from .views import EmpresaEmpreendedorRegisterView, AprendizRegisterView, activate

app_name = 'gerenciamento_registros'

urlpatterns = [
    # URLs para registro
    path('registro/empresa-empreendedor/', EmpresaEmpreendedorRegisterView.as_view(), name='registro_empresa_empreendedor'),
    path('registro/aprendiz/', AprendizRegisterView.as_view(), name='registro_aprendiz'),

    # URLs para o fluxo de ativação
    path('ativacao-enviada/', TemplateView.as_view(template_name='gerenciamento_registros/html/ativacao_enviada.html'), name='ativacao_enviada'),
    path('ativar/<str:uidb64>/<str:token>/', activate, name='ativar_conta'),
    path('ativacao/sucesso/', TemplateView.as_view(template_name='gerenciamento_registros/html/ativacao_sucesso.html'), name='ativacao_sucesso'),
    path('ativacao/invalida/', TemplateView.as_view(template_name='gerenciamento_registros/html/ativacao_invalida.html'), name='ativacao_invalida'),
]