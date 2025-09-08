# Arquivo: gerenciamento_acordos/views.py

from django.shortcuts import render
from .models import ConteudoApresentacaoAcordos

def pagina_inicial_acordos(request):
    conteudo_ativo = ConteudoApresentacaoAcordos.objects.filter(em_exibicao=True).first()
    context = {
        'conteudo_apresentacao': conteudo_ativo,
    }
    return render(request, 'gerenciamento_acordos/html/pagina_inicial_acordos.html', context)