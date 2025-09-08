# Arquivo: gerenciamento_aprenda/admin.py

from django.contrib import admin
from .models import ConteudoApresentacaoAprenda

# O modelo PalavraChaveAprenda não é mais necessário.
# @admin.register(PalavraChaveAprenda)
# class PalavraChaveAprendaAdmin(admin.ModelAdmin):
#     list_display = ('palavra', 'peso')
#     search_fields = ('palavra',)

@admin.register(ConteudoApresentacaoAprenda)
class ConteudoApresentacaoAprendaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'tipo_conteudo', 'em_exibicao')
    list_filter = ('tipo_conteudo', 'em_exibicao')
    search_fields = ('descricao',)