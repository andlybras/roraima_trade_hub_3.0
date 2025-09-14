from django.urls import path
from . import views

# app_name é essencial para que {% url 'aprenda:nome_da_url' %} funcione
app_name = 'aprenda'

urlpatterns = [
    # A URL raiz ('/aprenda-comex/') já está configurada, então esta é a página inicial do módulo
    path('', views.pagina_inicial_aprenda, name='pagina_inicial'),
    
    # Novas URLs que correspondem aos botões
    path('cursos-e-trilhas/', views.cursos_e_trilhas_view, name='cursos_e_trilhas'),
    path('ambiente-de-aprendizagem/', views.ambiente_aprendizagem_view, name='ambiente_aprendizagem'),
    path('links-uteis/', views.links_uteis_view, name='links_uteis'),
]