from django.shortcuts import render, get_object_or_404
from .models import Artigo

def detalhe_artigo(request, slug):
    artigo = get_object_or_404(Artigo, slug=slug, status='PUBLICADO')
    context = {
        'artigo': artigo,
    }
    return render(request, 'gerenciamento_artigos/html/detalhe_artigo.html', context)