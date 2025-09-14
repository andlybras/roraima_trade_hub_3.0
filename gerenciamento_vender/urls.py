from django.urls import path
from . import views

# app_name para que {% url 'vender:nome_da_url' %} funcione
app_name = 'vender'

urlpatterns = [
    # Página inicial do módulo '/quero-vender/'
    path('', views.pagina_inicial_vender, name='pagina_inicial'),

    # Novas URLs
    path('criar-perfil-empresarial/', views.criar_perfil_empresarial_view, name='criar_perfil_empresarial'),
    path('acessar-ambiente-empresarial/', views.acessar_ambiente_empresarial_view, name='acessar_ambiente_empresarial'),
]