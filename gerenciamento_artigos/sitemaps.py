from django.contrib.sitemaps import Sitemap
from .models import Artigo

class ArtigoSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Artigo.objects.filter(status='PUBLICADO')

    def lastmod(self, obj):
        return obj.data_atualizacao