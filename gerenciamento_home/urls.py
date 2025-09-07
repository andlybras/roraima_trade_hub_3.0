from django.urls import path
from . import views

app_name = 'gerenciamento_home'
urlpatterns = [
    path('', views.home, name='home'),
]