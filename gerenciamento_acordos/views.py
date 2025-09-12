# gerenciamento_acordos/views.py

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import ConteudoApresentacaoAcordos
from gerenciamento_artigos.models import Artigo

def pagina_inicial_acordos(request):
    conteudo_ativo = ConteudoApresentacaoAcordos.objects.filter(em_exibicao=True).first()
    context = {
        'conteudo_apresentacao': conteudo_ativo,
    }
    return render(request, 'gerenciamento_acordos/html/pagina_inicial_acordos.html', context)

def lista_artigos_por_categoria(request, slug_categoria):
    categoria_nome = dict(Artigo.CATEGORIA_CHOICES).get(slug_categoria)
    artigos = Artigo.objects.filter(categoria=slug_categoria, status='PUBLICADO').order_by('-data_publicacao')
    
    breadcrumbs = [
        {'nome': 'Início', 'url': reverse('gerenciamento_home:home')},
        {'nome': 'Acordos e Regulamentos', 'url': reverse('acordos:pagina_inicial')},
        {'nome': categoria_nome, 'url': ''},
    ]

    context = {
        'categoria_nome': categoria_nome,
        'artigos': artigos,
        'modulo_display': 'Acordos e Regulamentos',
        'url_voltar': 'acordos:pagina_inicial',
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'gerenciamento_artigos/html/lista_artigos.html', context)