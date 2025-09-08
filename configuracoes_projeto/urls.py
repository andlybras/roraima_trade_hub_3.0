from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gerenciamento_home.urls')),
    path('inteligencia-de-mercado/', include('gerenciamento_inteligencia_mercado.urls')),
    path('contas/', include('gerenciamento_registros.urls')),
]

# Adiciona as URLs de mídia em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
admin.site.site_header = "Painel Administrativo Roraima Trade Hub"
admin.site.site_title = "Administração Roraima Trade Hub"
admin.site.index_title = "Bem-vindo(a) ao painel de gerenciamento"