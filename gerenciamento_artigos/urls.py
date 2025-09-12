from django.urls import path
from . import views

app_name = 'artigos'

urlpatterns = [
    path('<slug:slug>/', views.detalhe_artigo, name='detalhe_artigo'),
]