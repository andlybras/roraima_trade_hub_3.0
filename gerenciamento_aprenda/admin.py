from django.contrib import admin
from .models import ConteudoApresentacaoAprenda

@admin.register(ConteudoApresentacaoAprenda)
class ConteudoApresentacaoAprendaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'tipo_conteudo', 'em_exibicao')
    list_filter = ('tipo_conteudo', 'em_exibicao')
    search_fields = ('descricao',)