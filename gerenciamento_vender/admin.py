from django.contrib import admin
from .models import ConteudoApresentacaoVender

@admin.register(ConteudoApresentacaoVender)
class ConteudoApresentacaoVenderAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'tipo_conteudo', 'em_exibicao')
    list_filter = ('tipo_conteudo', 'em_exibicao')
    search_fields = ('descricao',)