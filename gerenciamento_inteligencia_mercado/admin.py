# Arquivo: gerenciamento_inteligencia_mercado/admin.py

from django.contrib import admin
from .models import ConteudoInteligencia, Grafico, TermoGlossario

@admin.register(ConteudoInteligencia)
class ConteudoInteligenciaAdmin(admin.ModelAdmin):
    list_display = ('titulo_card', 'categoria', 'titulo_pagina')
    list_filter = ('categoria',)
    search_fields = ('titulo_card', 'titulo_pagina')

@admin.register(Grafico)
class GraficoAdmin(admin.ModelAdmin):
    # ALTERAÇÃO: Adicionamos o campo 'tag_para_copiar'
    list_display = ('titulo', 'tag_para_copiar', 'is_grafico_principal')
    search_fields = ('titulo',)
    readonly_fields = ('tag_para_copiar',) # O usuário não pode editar a tag diretamente

    # Nova função que cria a tag formatada
    def tag_para_copiar(self, obj):
        if obj.chave:
            return f"[grafico:{obj.chave}]"
        return "Salve o gráfico para gerar a chave."
    tag_para_copiar.short_description = "Tag para Copiar e Colar"

@admin.register(TermoGlossario)
class TermoGlossarioAdmin(admin.ModelAdmin):
    list_display = ('termo',)
    search_fields = ('termo',)