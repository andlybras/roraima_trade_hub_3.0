from django.shortcuts import render, get_object_or_404
from .models import ConteudoApresentacaoAcordos
from gerenciamento_artigos.models import Artigo, CategoriaArtigo

def pagina_inicial_acordos(request):
    conteudo_ativo = ConteudoApresentacaoAcordos.objects.filter(em_exibicao=True).first()
    categorias = CategoriaArtigo.objects.filter(modulo='ACORDOS')   
    context = {
        'conteudo_apresentacao': conteudo_ativo,
        'categorias': categorias,
    }
    return render(request, 'gerenciamento_acordos/html/pagina_inicial_acordos.html', context)

def lista_artigos_por_categoria(request, slug_categoria):
    categoria = get_object_or_404(CategoriaArtigo, slug=slug_categoria, modulo='ACORDOS')
    artigos = Artigo.objects.filter(categoria=categoria, status='PUBLICADO').order_by('-data_publicacao')
    
    context = {
        'categoria': categoria,
        'artigos': artigos,
        'modulo_display': 'Acordos e Regulamentos',
        'url_voltar': 'acordos:pagina_inicial'
    }
    return render(request, 'gerenciamento_artigos/html/lista_artigos.html', context)