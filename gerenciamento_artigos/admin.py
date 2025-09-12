# gerenciamento_artigos/admin.py

from django.contrib import admin
from .models import Artigo

@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'tipo_conteudo', 'status', 'data_publicacao', 'autor')
    list_filter = ('status', 'categoria', 'tipo_conteudo')
    search_fields = ('titulo', 'subtitulo')
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'data_publicacao'
    
    fieldsets = (
        ('Identificação do Artigo', {
            'fields': ('categoria', 'titulo', 'slug', 'subtitulo', 'imagem_card')
        }),
        ('Conteúdo Principal', {
            'description': "Escolha o tipo de conteúdo e preencha os campos correspondentes abaixo.",
            # CAMPO 'resumo_destaque' ADICIONADO AQUI
            'fields': ('resumo_destaque', 'tipo_conteudo', 'corpo_conteudo', 'arquivo_pdf')
        }),
        ('Publicação', {
            'fields': ('status', 'data_publicacao')
        }),
        ('SEO (Otimização para Buscadores)', {
            'classes': ('collapse',),
            'fields': ('meta_descricao', 'palavras_chave'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.autor = request.user
        super().save_model(request, obj, form, change)