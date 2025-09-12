from django.contrib import admin
from .models import Categoria, Noticia, NoticiaDestaque, BannerNoticias
from django.utils.html import format_html

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug')
    search_fields = ('nome',)
    prepopulated_fields = {'slug': ('nome',)}

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'status', 'data_publicacao', 'imagem_card_thumbnail')
    list_filter = ('status', 'categorias', 'data_publicacao')
    search_fields = ('titulo', 'subtitulo', 'corpo')
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'data_publicacao'
    readonly_fields = ('autor',)
    
    # Organiza os campos em seções para melhor usabilidade
    fieldsets = (
        ('Conteúdo Principal', {
            'fields': ('titulo', 'slug', 'subtitulo', 'corpo')
        }),
        ('Imagens', {
            'fields': ('imagem_card', 'imagem_destaque')
        }),
        ('Organização e Publicação', {
            'fields': ('status', 'categorias', 'tags', 'data_publicacao')
        }),
        ('SEO (Otimização para Buscadores)', {
            'classes': ('collapse',), # Começa fechado para não poluir
            'fields': ('meta_descricao', 'palavras_chave'),
        }),
    )

    # Habilita o botão "Ver no site"
    view_on_site = True

    def save_model(self, request, obj, form, change):
        if not obj.autor_id:
            obj.autor = request.user
        super().save_model(request, obj, form, change)
    
    # Função para mostrar a miniatura da imagem
    def imagem_card_thumbnail(self, obj):
        if obj.imagem_card:
            return format_html('<img src="{}" width="100" />', obj.imagem_card.url)
        return "Sem imagem"
    imagem_card_thumbnail.short_description = 'Miniatura do Card'


@admin.register(NoticiaDestaque)
class NoticiaDestaqueAdmin(admin.ModelAdmin):
    list_display = ('noticia', 'ordem')
    list_editable = ('ordem',)
    raw_id_fields = ('noticia',)

@admin.register(BannerNoticias)
class BannerNoticiasAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ativo')
    list_filter = ('ativo',)