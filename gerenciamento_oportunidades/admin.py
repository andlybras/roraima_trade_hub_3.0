from django.contrib import admin
from .models import ConteudoApresentacaoOportunidades

@admin.register(ConteudoApresentacaoOportunidades)
class ConteudoApresentacaoOportunidadesAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'tipo_conteudo', 'em_exibicao')
    list_filter = ('tipo_conteudo', 'em_exibicao')