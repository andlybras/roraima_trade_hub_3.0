# Arquivo: gerenciamento_home/admin.py

from django.contrib import admin
from .models import HeaderLogo, ImagemApresentacao, PartnerLogo

@admin.register(HeaderLogo)
class HeaderLogoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'link_url')
    search_fields = ('descricao',)

@admin.register(ImagemApresentacao)
class ImagemApresentacaoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'descricao', 'ordem', 'link_url')
    list_filter = ('tipo',)
    search_fields = ('descricao',)

@admin.register(PartnerLogo)
class PartnerLogoAdmin(admin.ModelAdmin):
    list_display = ('nome_parceiro', 'ordem', 'link_url')
    search_fields = ('nome_parceiro',)