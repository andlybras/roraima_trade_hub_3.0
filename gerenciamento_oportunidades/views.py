from django.shortcuts import render
from .models import ConteudoApresentacaoOportunidades

def pagina_inicial_oportunidades(request):
    conteudo_ativo = ConteudoApresentacaoOportunidades.objects.filter(em_exibicao=True).first()
    context = {'conteudo_apresentacao': conteudo_ativo}
    return render(request, 'gerenciamento_oportunidades/html/pagina_inicial_oportunidades.html', context)