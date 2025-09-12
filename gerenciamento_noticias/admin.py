from django.contrib import admin
from .models import Categoria, Noticia, NoticiaDestaque, BannerNoticias

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug')
    search_fields = ('nome',)
    prepopulated_fields = {'slug': ('nome',)}

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'status', 'data_publicacao')
    list_filter = ('status', 'categorias', 'data_publicacao')
    search_fields = ('titulo', 'subtitulo', 'corpo')
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'data_publicacao'
    readonly_fields = ('autor',)

    def save_model(self, request, obj, form, change):
        if not obj.autor_id:
            obj.autor = request.user
        super().save_model(request, obj, form, change)

@admin.register(NoticiaDestaque)
class NoticiaDestaqueAdmin(admin.ModelAdmin):
    list_display = ('noticia', 'ordem')
    list_editable = ('ordem',)
    raw_id_fields = ('noticia',)
    
@admin.register(BannerNoticias)
class BannerNoticiasAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ativo')
    list_filter = ('ativo',)