from django.urls import path
from . import views

app_name = 'oportunidades'

urlpatterns = [
    path('', views.pagina_inicial_oportunidades, name='pagina_inicial'),
    path('<slug:slug_categoria>/', views.lista_artigos_por_categoria, name='lista_por_categoria'),
]