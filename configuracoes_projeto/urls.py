from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gerenciamento_home.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('noticias/', include('gerenciamento_noticias.urls', namespace='noticias')),
    path('inteligencia-de-mercado/', include('gerenciamento_inteligencia_mercado.urls')),
    path('aprenda-comex/', include('gerenciamento_aprenda.urls')),
    path('quero-vender/', include('gerenciamento_vender.urls')),
    path('acordos-e-regulamentos/', include('gerenciamento_acordos.urls')),
    path('oportunidades/', include('gerenciamento_oportunidades.urls')),
    path('destino-roraima/', include('gerenciamento_destino.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
admin.site.site_header = "Painel Administrativo Roraima Trade Hub"
admin.site.site_title = "Administração Roraima Trade Hub"
admin.site.index_title = "Bem-vindo(a) ao painel de gerenciamento"