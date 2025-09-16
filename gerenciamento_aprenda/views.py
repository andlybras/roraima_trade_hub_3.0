from django.shortcuts import render
from .models import ConteudoApresentacaoAprenda
from django.http import HttpResponse

def pagina_inicial_aprenda(request):
    conteudo_ativo = ConteudoApresentacaoAprenda.objects.filter(em_exibicao=True).first()
    context = {
        'titulo_pagina': 'Aprenda Comex',
        'conteudo_apresentacao': conteudo_ativo,
    }
    return render(request, 'gerenciamento_aprenda/html/pagina_inicial_aprenda.html', context)

def cursos_e_trilhas_view(request):
    return HttpResponse("<h1>Página de Cursos e Trilhas de Aprendizagem (Em Construção)</h1>")

def ambiente_aprendizagem_view(request):
    return HttpResponse("<h1>Página de Acesso ao Ambiente de Aprendizagem (Em Construção)</h1>")

def links_uteis_view(request):
    return HttpResponse("<h1>Página de Links Úteis (Em Construção)</h1>")