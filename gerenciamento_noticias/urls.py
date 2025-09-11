from django.urls import path
from .views import PaginaInicialNoticias, DetalheNoticia, NoticiasPorCategoria, mais_noticias_ajax

app_name = 'noticias'

urlpatterns = [
    path('', PaginaInicialNoticias.as_view(), name='lista_noticias'),
    path('categoria/<slug:slug>/', NoticiasPorCategoria.as_view(), name='noticias_por_categoria'),
    path('mais-noticias/', mais_noticias_ajax, name='mais_noticias_ajax'),
    path('<slug:slug>/', DetalheNoticia.as_view(), name='detalhe_noticia'),
]