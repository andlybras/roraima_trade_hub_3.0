from django.urls import path
from . import views

app_name = 'aprenda'

urlpatterns = [
    path('', views.pagina_inicial_aprenda, name='pagina_inicial'),
    path('cursos-e-trilhas/', views.cursos_e_trilhas_view, name='cursos_e_trilhas'),
    path('ambiente-de-aprendizagem/', views.ambiente_aprendizagem_view, name='ambiente_aprendizagem'),
    path('links-uteis/', views.links_uteis_view, name='links_uteis'),
]