# gerenciamento_artigos/sitemaps.py

from django.contrib.sitemaps import Sitemap
from .models import Artigo

class ArtigoSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        # Retorna todos os artigos que estão com status 'PUBLICADO'
        return Artigo.objects.filter(status='PUBLICADO')

    def lastmod(self, obj):
        # Usa a data da última atualização para informar o Google
        return obj.data_atualizacao