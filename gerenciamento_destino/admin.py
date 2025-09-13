# gerenciamento_destino/admin.py

from django.contrib import admin
from .models import (
    ConteudoApresentacaoDestino, Categoria, 
    PontoDeInteresse, ImagemGaleria, 
    Roteiro, OrdemPontoRoteiro
)
# O import de ServicoTuristico foi removido

@admin.register(ConteudoApresentacaoDestino)
class ConteudoApresentacaoDestinoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'tipo_conteudo', 'em_exibicao')
    list_filter = ('tipo_conteudo', 'em_exibicao')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'grupo')
    list_filter = ('grupo',)
    search_fields = ('nome',)
    prepopulated_fields = {'slug': ('nome',)}

class ImagemGaleriaInline(admin.TabularInline):
    model = ImagemGaleria
    extra = 1
    fields = ('imagem', 'legenda')
    verbose_name = "Imagem da Galeria"
    verbose_name_plural = "Galeria de Imagens"

@admin.register(PontoDeInteresse)
class PontoDeInteresseAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'publicado')
    list_filter = ('categoria', 'publicado')
    search_fields = ('titulo', 'descricao_curta')
    prepopulated_fields = {'slug': ('titulo',)}
    inlines = [ImagemGaleriaInline]
    autocomplete_fields = ['categoria']

# O registro do ServicoTuristicoAdmin foi completamente removido

class OrdemPontoRoteiroInline(admin.TabularInline):
    model = OrdemPontoRoteiro
    extra = 1
    autocomplete_fields = ['ponto_de_interesse']
    verbose_name = "Ponto de Interesse no Roteiro"
    verbose_name_plural = "Pontos de Interesse neste Roteiro"

@admin.register(Roteiro)
class RoteiroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'publicado')
    search_fields = ('titulo',)
    list_filter = ('publicado',)
    prepopulated_fields = {'slug': ('titulo',)}
    inlines = [OrdemPontoRoteiroInline]