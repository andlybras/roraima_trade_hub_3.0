from django.shortcuts import render
from .models import ConteudoApresentacaoVender

def pagina_inicial_vender(request):
    conteudo_ativo = ConteudoApresentacaoVender.objects.filter(em_exibicao=True).first()
    context = {
        'titulo_pagina': 'Quero Vender',
        'conteudo_apresentacao': conteudo_ativo,
    }
    return render(request, 'gerenciamento_vender/html/pagina_inicial_vender.html', context)