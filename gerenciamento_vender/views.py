from django.shortcuts import render
from .models import ConteudoApresentacaoVender
from django.http import HttpResponse

def pagina_inicial_vender(request):
    conteudo_ativo = ConteudoApresentacaoVender.objects.filter(em_exibicao=True).first()
    context = {
        'titulo_pagina': 'Quero Vender',
        'conteudo_apresentacao': conteudo_ativo,
    }
    return render(request, 'gerenciamento_vender/html/pagina_inicial_vender.html', context)

# --- Nossas novas views (funções) ---

# View para a página "Crie seu Perfil Empresarial"
def criar_perfil_empresarial_view(request):
    return HttpResponse("<h1>Página para Criação de Perfil Empresarial (Em Construção)</h1>")

# View para a página "Acesse seu Ambiente Empresarial"
def acessar_ambiente_empresarial_view(request):
    return HttpResponse("<h1>Página de Acesso ao Ambiente Empresarial (Em Construção)</h1>")