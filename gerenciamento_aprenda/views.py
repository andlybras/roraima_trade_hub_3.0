# Arquivo: gerenciamento_aprenda/views.py

from django.shortcuts import render
from .models import ConteudoApresentacaoAprenda

def pagina_inicial_aprenda(request):
    """
    Renderiza a página inicial do módulo Aprenda Comex,
    exibindo o conteúdo de apresentação ativo.
    """
    # Busca o único conteúdo que deve estar em exibição
    conteudo_ativo = ConteudoApresentacaoAprenda.objects.filter(em_exibicao=True).first()

    context = {
        'titulo_pagina': 'Aprenda Comex',
        'conteudo_apresentacao': conteudo_ativo,
    }
    return render(request, 'gerenciamento_aprenda/html/pagina_inicial_aprenda.html', context)