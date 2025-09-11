from django.urls import path
from .views import PaginaInicialNoticias, DetalheNoticia, NoticiasPorCategoria, mais_noticias_ajax, NoticiasPorTag, BuscaNoticias

app_name = 'noticias'

urlpatterns = [
    path('', PaginaInicialNoticias.as_view(), name='lista_noticias'),
    path('busca/', BuscaNoticias.as_view(), name='busca_noticias'),
    path('categoria/<slug:slug>/', NoticiasPorCategoria.as_view(), name='noticias_por_categoria'),
    path('tag/<slug:slug>/', NoticiasPorTag.as_view(), name='noticias_por_tag'),
    path('mais-noticias/', mais_noticias_ajax, name='mais_noticias_ajax'),
    path('<slug:slug>/', DetalheNoticia.as_view(), name='detalhe_noticia'),
]