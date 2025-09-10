from django.shortcuts import render
from .models import ConteudoApresentacaoAprenda
from gerenciamento_registros.decorators import educacional_required

def pagina_inicial_aprenda(request):
    conteudo_ativo = ConteudoApresentacaoAprenda.objects.filter(em_exibicao=True).first()
    context = {
        'titulo_pagina': 'Aprenda Comex',
        'conteudo_apresentacao': conteudo_ativo,
    }
    return render(request, 'gerenciamento_aprenda/html/pagina_inicial_aprenda.html', context)

@educacional_required
def dashboard_educacional_view(request):
    return render(request, 'gerenciamento_aprenda/html/dashboard_educacional.html')