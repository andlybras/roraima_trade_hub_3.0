from django.shortcuts import render, get_object_or_404
from .models import ConteudoApresentacaoOportunidades
from gerenciamento_artigos.models import Artigo, CategoriaArtigo

def pagina_inicial_oportunidades(request):
    conteudo_ativo = ConteudoApresentacaoOportunidades.objects.filter(em_exibicao=True).first()
    categorias = CategoriaArtigo.objects.filter(modulo='OPORTUNIDADES')
    context = {
        'conteudo_apresentacao': conteudo_ativo,
        'categorias': categorias,
    }
    return render(request, 'gerenciamento_oportunidades/html/pagina_inicial_oportunidades.html', context)

def lista_artigos_por_categoria(request, slug_categoria):
    categoria = get_object_or_404(CategoriaArtigo, slug=slug_categoria, modulo='OPORTUNIDADES')
    artigos = Artigo.objects.filter(categoria=categoria, status='PUBLICADO').order_by('-data_publicacao')
    
    context = {
        'categoria': categoria,
        'artigos': artigos,
        'modulo_display': 'Oportunidades',
        'url_voltar': 'oportunidades:pagina_inicial'
    }
    return render(request, 'gerenciamento_artigos/html/lista_artigos.html', context)