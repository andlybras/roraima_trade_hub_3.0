# gerenciamento_destino/views.py

from django.shortcuts import render, get_object_or_404
from .models import ConteudoApresentacaoDestino, Categoria, PontoDeInteresse
from django.urls import reverse # Importamos a ferramenta 'reverse'

def pagina_inicial_destino(request):
    conteudo_ativo = ConteudoApresentacaoDestino.objects.filter(em_exibicao=True).first()
    context = {'conteudo_apresentacao': conteudo_ativo}
    return render(request, 'gerenciamento_destino/html/pagina_inicial_destino.html', context)

def mapa_categoria_view(request, categoria_slug):
    categoria = get_object_or_404(Categoria, slug=categoria_slug)
    pontos = PontoDeInteresse.objects.filter(categoria=categoria, publicado=True)

    pontos_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        float(str(ponto.longitude).replace(',', '.')),
                        float(str(ponto.latitude).replace(',', '.'))
                    ],
                },
                "properties": {
                    "titulo": ponto.titulo,
                    "descricao_curta": ponto.descricao_curta,
                    "imagem_url": ponto.imagem_principal.url if ponto.imagem_principal else '',
                    # ADIÇÃO: Criamos o link para a página de detalhes de cada ponto
                    "detalhe_url": reverse('destino:detalhe_ponto', args=[ponto.slug])
                }
            } for ponto in pontos
        ]
    }

    context = {
        'categoria': categoria,
        'pontos_geojson': pontos_geojson,
        'tem_pontos': pontos.exists()
    }
    
    return render(request, 'gerenciamento_destino/html/mapa_interativo.html', context)

# --- NOVA VIEW PARA A PÁGINA DE DETALHES ---
def detalhe_ponto_view(request, ponto_slug):
    # Busca o Ponto de Interesse específico pelo seu "apelido" (slug) na URL
    ponto = get_object_or_404(PontoDeInteresse, slug=ponto_slug, publicado=True)
    
    context = {
        'ponto': ponto
    }
    
    # Esta view vai usar um novo template que ainda vamos criar
    return render(request, 'gerenciamento_destino/html/detalhe_ponto.html', context)