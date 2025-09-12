# gerenciamento_destino/admin.py

from django.contrib import admin
from .models import (
    ConteudoApresentacaoDestino, Categoria, 
    PontoDeInteresse, ImagemGaleria, ServicoTuristico, 
    Roteiro, OrdemPontoRoteiro
)

# SEU MODELO ORIGINAL - MANTIDO E REGISTRADO
@admin.register(ConteudoApresentacaoDestino)
class ConteudoApresentacaoDestinoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'tipo_conteudo', 'em_exibicao')
    list_filter = ('tipo_conteudo', 'em_exibicao')

# --- REGISTRO DOS NOVOS MODELOS ---

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('nome',)
    prepopulated_fields = {'slug': ('nome',)}

class ImagemGaleriaInline(admin.TabularInline):
    model = ImagemGaleria
    extra = 1  # Quantos campos de upload de imagem extra aparecem
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
    
    fieldsets = (
        ('Informações Principais', {
            'fields': ('titulo', 'slug', 'categoria', 'publicado')
        }),
        ('Conteúdo e Mídia', {
            'fields': ('descricao_curta', 'imagem_principal', 'descricao_completa')
        }),
        ('Localização no Mapa', {
            'fields': ('latitude', 'longitude'),
            'description': 'Use um site como o Google Maps para obter as coordenadas. Clique com o botão direito no local e o primeiro item será a latitude e longitude.'
        }),
        ('Dicas para o Turista', {
            'fields': ('informacoes_praticas',)
        }),
    )

@admin.register(ServicoTuristico)
class ServicoTuristicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'telefone', 'publicado')
    list_filter = ('categoria', 'publicado')
    search_fields = ('nome', 'descricao', 'endereco')

class OrdemPontoRoteiroInline(admin.TabularInline):
    model = OrdemPontoRoteiro
    extra = 1
    autocomplete_fields = ['ponto_de_interesse'] # Facilita a busca
    verbose_name = "Ponto de Interesse no Roteiro"
    verbose_name_plural = "Pontos de Interesse neste Roteiro"

@admin.register(Roteiro)
class RoteiroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'publicado')
    search_fields = ('titulo',)
    list_filter = ('publicado',)
    prepopulated_fields = {'slug': ('titulo',)}
    inlines = [OrdemPontoRoteiroInline]
    
    # Adicionando autocomplete para o campo 'ponto_de_interesse' no inline
    # Requer que o admin do PontoDeInteresse tenha 'search_fields' definido
    def get_form(self, request, obj=None, **kwargs):
        # Habilitar busca para PontoDeInteresseAdmin
        self.search_fields = ('titulo',) 
        return super().get_form(request, obj, **kwargs)