from django.urls import path
from . import views

app_name = 'acordos'

urlpatterns = [
    path('', views.pagina_inicial_acordos, name='pagina_inicial'),
]