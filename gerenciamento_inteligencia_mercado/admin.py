# Arquivo: gerenciamento_inteligencia_mercado/admin.py

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import ConteudoInteligencia, Grafico, TermoGlossario

@admin.register(ConteudoInteligencia)
class ConteudoInteligenciaAdmin(admin.ModelAdmin):
    # ADICIONADO: 'publicado' e 'imagem_thumbnail'
    list_display = ('titulo_card', 'categoria', 'publicado', 'imagem_thumbnail')
    list_filter = ('categoria', 'publicado') # Adicionado filtro por status
    search_fields = ('titulo_card', 'titulo_pagina')
    
    # Adiciona um campo de preview da imagem
    def imagem_thumbnail(self, obj):
        if obj.imagem_card:
            return format_html('<img src="{}" width="100" />', obj.imagem_card.url)
        return "Sem imagem"
    imagem_thumbnail.short_description = 'Miniatura da Imagem'

@admin.register(Grafico)
class GraficoAdmin(admin.ModelAdmin):
    # ADICIONADO: 'preview_link'
    list_display = ('titulo', 'tipo_grafico', 'tag_para_copiar', 'is_grafico_principal', 'preview_link')
    list_filter = ('tipo_grafico', 'is_grafico_principal') # Adicionado filtros
    search_fields = ('titulo',)
    readonly_fields = ('tag_para_copiar', 'preview_link')

    def tag_para_copiar(self, obj):
        if obj.chave:
            return f"[grafico:{obj.chave}]"
        return "Salve o gráfico para gerar a chave."
    tag_para_copiar.short_description = "Tag para Copiar"
    
    # Adiciona o link de preview
    def preview_link(self, obj):
        if obj.pk:
            url = reverse('inteligencia:grafico_preview', args=[obj.pk])
            return format_html('<a href="{}" target="_blank">Pré-visualizar</a>', url)
        return "Salve para poder pré-visualizar"
    preview_link.short_description = 'Preview'

@admin.register(TermoGlossario)
class TermoGlossarioAdmin(admin.ModelAdmin):
    list_display = ('termo',)
    search_fields = ('termo',)