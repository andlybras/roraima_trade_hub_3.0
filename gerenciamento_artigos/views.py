# gerenciamento_artigos/views.py

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Artigo

def detalhe_artigo(request, slug):
    artigo = get_object_or_404(Artigo, slug=slug, status='PUBLICADO')

    # Lógica para saber a qual módulo o artigo pertence e montar o breadcrumb
    categoria_slug = artigo.categoria
    categoria_nome = dict(Artigo.CATEGORIA_CHOICES).get(categoria_slug)
    
    acordos_cats = ['legislacao-fiscal-e-aduaneira', 'acordos-comerciais', 'regulamentos-internacionais']
    
    if categoria_slug in acordos_cats:
        modulo_nome = 'Acordos e Regulamentos'
        modulo_url = reverse('acordos:pagina_inicial')
        categoria_url = reverse('acordos:lista_por_categoria', kwargs={'slug_categoria': categoria_slug})
    else:
        modulo_nome = 'Oportunidades'
        modulo_url = reverse('oportunidades:pagina_inicial')
        categoria_url = reverse('oportunidades:lista_por_categoria', kwargs={'slug_categoria': categoria_slug})

    breadcrumbs = [
        {'nome': 'Início', 'url': reverse('gerenciamento_home:home')},
        {'nome': modulo_nome, 'url': modulo_url},
        {'nome': categoria_nome, 'url': categoria_url},
        {'nome': artigo.titulo[:30] + '...', 'url': ''}, # Mostra só um pedaço do título
    ]

    context = {
        'artigo': artigo,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'gerenciamento_artigos/html/detalhe_artigo.html', context)