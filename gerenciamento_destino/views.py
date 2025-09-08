from django.shortcuts import render
from .models import ConteudoApresentacaoDestino

def pagina_inicial_destino(request):
    conteudo_ativo = ConteudoApresentacaoDestino.objects.filter(em_exibicao=True).first()
    context = {'conteudo_apresentacao': conteudo_ativo}
    return render(request, 'gerenciamento_destino/html/pagina_inicial_destino.html', context)