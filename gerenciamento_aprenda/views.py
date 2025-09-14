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

# --- Nossas novas views (funções) ---

# View para a página "Cursos e Trilhas de Aprendizagem"
def cursos_e_trilhas_view(request):
    # Por enquanto, retorna uma resposta simples. No futuro, aqui listaremos os cursos.
    return HttpResponse("<h1>Página de Cursos e Trilhas de Aprendizagem (Em Construção)</h1>")

# View para a página "Acesse o Ambiente de Aprendizagem"
def ambiente_aprendizagem_view(request):
    # Por enquanto, retorna uma resposta simples. No futuro, pode redirecionar para um sistema de EAD.
    return HttpResponse("<h1>Página de Acesso ao Ambiente de Aprendizagem (Em Construção)</h1>")

# View para a página "Links Úteis"
def links_uteis_view(request):
    # Por enquanto, retorna uma resposta simples. No futuro, listaremos os links.
    return HttpResponse("<h1>Página de Links Úteis (Em Construção)</h1>")