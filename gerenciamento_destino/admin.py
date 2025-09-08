from django.contrib import admin
from .models import ConteudoApresentacaoDestino

@admin.register(ConteudoApresentacaoDestino)
class ConteudoApresentacaoDestinoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'tipo_conteudo', 'em_exibicao')
    list_filter = ('tipo_conteudo', 'em_exibicao')