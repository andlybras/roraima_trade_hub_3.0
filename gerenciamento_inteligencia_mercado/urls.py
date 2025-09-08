from django.urls import path
from . import views

app_name = 'inteligencia'

urlpatterns = [
    path('', views.pagina_inicial_inteligencia, name='pagina_inicial'),
    path('glossario/', views.glossario_view, name='glossario'),
    path('conteudo/<int:pk>/', views.detalhe_conteudo, name='detalhe_conteudo'),
    path('<str:categoria>/', views.lista_conteudo_por_categoria, name='lista_por_categoria'),
    path('grafico/preview/<int:pk>/', views.grafico_preview_view, name='grafico_preview'),
]