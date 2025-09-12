# gerenciamento_oportunidades/views.py

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import ConteudoApresentacaoOportunidades
from gerenciamento_artigos.models import Artigo

def pagina_inicial_oportunidades(request):
    conteudo_ativo = ConteudoApresentacaoOportunidades.objects.filter(em_exibicao=True).first()
    context = {
        'conteudo_apresentacao': conteudo_ativo,
    }
    return render(request, 'gerenciamento_oportunidades/html/pagina_inicial_oportunidades.html', context)

def lista_artigos_por_categoria(request, slug_categoria):
    categoria_nome = dict(Artigo.CATEGORIA_CHOICES).get(slug_categoria)
    artigos = Artigo.objects.filter(categoria=slug_categoria, status='PUBLICADO').order_by('-data_publicacao')
    
    breadcrumbs = [
        {'nome': 'Início', 'url': reverse('gerenciamento_home:home')},
        {'nome': 'Oportunidades', 'url': reverse('oportunidades:pagina_inicial')},
        {'nome': categoria_nome, 'url': ''},
    ]
    
    context = {
        'categoria_nome': categoria_nome,
        'artigos': artigos,
        'modulo_display': 'Oportunidades',
        'url_voltar': 'oportunidades:pagina_inicial',
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'gerenciamento_artigos/html/lista_artigos.html', context)