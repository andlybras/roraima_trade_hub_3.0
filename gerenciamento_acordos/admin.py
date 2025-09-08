# Arquivo: gerenciamento_acordos/admin.py

from django.contrib import admin
from .models import ConteudoApresentacaoAcordos

@admin.register(ConteudoApresentacaoAcordos)
class ConteudoApresentacaoAcordosAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'tipo_conteudo', 'em_exibicao')
    list_filter = ('tipo_conteudo', 'em_exibicao')