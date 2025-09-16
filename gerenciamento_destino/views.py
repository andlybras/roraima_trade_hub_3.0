from django.shortcuts import render, get_object_or_404
from .models import ConteudoApresentacaoDestino, Categoria, PontoDeInteresse, Roteiro
from django.urls import reverse
from django.http import JsonResponse
import json

def pagina_inicial_destino(request):
    conteudo_ativo = ConteudoApresentacaoDestino.objects.filter(em_exibicao=True).first()
    context = {'conteudo_apresentacao': conteudo_ativo}
    return render(request, 'gerenciamento_destino/html/pagina_inicial_destino.html', context)

def detalhe_ponto_view(request, ponto_slug):
    ponto = get_object_or_404(PontoDeInteresse, slug=ponto_slug, publicado=True)
    breadcrumbs = [{'nome': 'Início', 'url': reverse('gerenciamento_home:home')},{'nome': 'Destino Roraima', 'url': reverse('destino:pagina_inicial')},]
    if ponto.categoria.grupo == 'NATUREZA':
        breadcrumbs.append({'nome': 'Belezas da Natureza', 'url': reverse('destino:belezas_da_natureza')})
    elif ponto.categoria.grupo == 'CULTURA':
        breadcrumbs.append({'nome': 'Cultura e Tradições', 'url': reverse('destino:cultura_e_tradicoes')})
    breadcrumbs.append({'nome': ponto.titulo, 'url': ''})
    context = {'ponto': ponto, 'breadcrumbs': breadcrumbs}
    return render(request, 'gerenciamento_destino/html/detalhe_ponto.html', context)

def detalhe_roteiro_view(request, roteiro_slug):
    roteiro = get_object_or_404(Roteiro, slug=roteiro_slug, publicado=True)
    pontos_ordenados = roteiro.pontos_de_interesse.order_by('ordempontoroteiro__ordem')

    breadcrumbs = [
        {'nome': 'Início', 'url': reverse('gerenciamento_home:home')},
        {'nome': 'Destino Roraima', 'url': reverse('destino:pagina_inicial')},
        {'nome': 'Roteiros Temáticos', 'url': reverse('destino:lista_roteiros')},
        {'nome': roteiro.titulo, 'url': ''},
    ]
    
    pontos_geojson = {"type": "FeatureCollection", "features": [
        {"type": "Feature",
         "geometry": {"type": "Point", "coordinates": [p.longitude, p.latitude]},
         "properties": {
             "titulo": p.titulo,
             "detalhe_url": reverse('destino:detalhe_ponto', args=[p.slug]),
         }
        } for p in pontos_ordenados
    ]}
    
    context = {
        'roteiro': roteiro,
        'pontos': pontos_ordenados,
        'pontos_geojson': pontos_geojson,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'gerenciamento_destino/html/detalhe_roteiro.html', context)

def detalhe_roteiro_view(request, roteiro_slug):
    roteiro = get_object_or_404(Roteiro, slug=roteiro_slug, publicado=True)

    pontos_ordenados = roteiro.pontos_de_interesse.order_by('ordempontoroteiro__ordem')

    breadcrumbs = [
        {'nome': 'Início', 'url': reverse('gerenciamento_home:home')},
        {'nome': 'Destino Roraima', 'url': reverse('destino:pagina_inicial')},
        {'nome': 'Roteiros Temáticos', 'url': reverse('destino:lista_roteiros')},
        {'nome': roteiro.titulo, 'url': ''},
    ]
    
    pontos_geojson = {"type": "FeatureCollection", "features": [
        {"type": "Feature",
         "geometry": {"type": "Point", "coordinates": [p.longitude, p.latitude]},
         "properties": {
             "titulo": p.titulo,
             "detalhe_url": reverse('destino:detalhe_ponto', args=[p.slug]),
         }
        } for p in pontos_ordenados
    ]}
    
    context = {
        'roteiro': roteiro,
        'pontos': pontos_ordenados,
        'pontos_geojson': pontos_geojson,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'gerenciamento_destino/html/detalhe_roteiro.html', context)

def meu_roteiro_view(request):
    breadcrumbs = [{'nome': 'Início', 'url': reverse('gerenciamento_home:home')},{'nome': 'Destino Roraima', 'url': reverse('destino:pagina_inicial')},{'nome': 'Meu Roteiro', 'url': ''}]
    context = {'breadcrumbs': breadcrumbs}
    return render(request, 'gerenciamento_destino/html/meu_roteiro.html', context)

def dados_roteiro_api_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            slugs = data.get('slugs', [])
            pontos_qs = PontoDeInteresse.objects.filter(slug__in=slugs, publicado=True)
            pontos_dict = {p.slug: p for p in pontos_qs}
            pontos_ordenados = [pontos_dict[slug] for slug in slugs if slug in pontos_dict]
            dados_para_js = []
            for ponto in pontos_ordenados:
                dados_para_js.append({'titulo': ponto.titulo,'slug': ponto.slug,'descricao_curta': ponto.descricao_curta,'imagem_url': ponto.imagem_principal.url if ponto.imagem_principal else '','detalhe_url': reverse('destino:detalhe_ponto', args=[ponto.slug]),'latitude': float(str(ponto.latitude).replace(',', '.')),'longitude': float(str(ponto.longitude).replace(',', '.')),})
            return JsonResponse({'pontos': dados_para_js})
        except json.JSONDecodeError:
            return JsonResponse({'erro': 'JSON inválido'}, status=400)
    return JsonResponse({'erro': 'Apenas requisições POST são permitidas'}, status=405)

def belezas_da_natureza_view(request):
    pontos = PontoDeInteresse.objects.filter(publicado=True, categoria__grupo='NATUREZA')
    categorias_filtros = Categoria.objects.filter(grupo='NATUREZA')
    
    breadcrumbs = [
        {'nome': 'Início', 'url': reverse('gerenciamento_home:home')},
        {'nome': 'Destino Roraima', 'url': reverse('destino:pagina_inicial')},
        {'nome': 'Belezas da Natureza', 'url': ''},
    ]

    pontos_geojson = {"type": "FeatureCollection", "features": [
        {"type": "Feature", 
         "geometry": {"type": "Point", "coordinates": [float(str(p.longitude).replace(',', '.')), float(str(p.latitude).replace(',', '.'))]},
         "properties": {
             "titulo": p.titulo, "descricao_curta": p.descricao_curta, 
             "imagem_url": p.imagem_principal.url if p.imagem_principal else '', 
             "detalhe_url": reverse('destino:detalhe_ponto', args=[p.slug]), 
             "slug": p.slug,
             "categoria_slug": p.categoria.slug,
             "icone_url": p.categoria.icone.url if p.categoria.icone else None
            }
        } for p in pontos]}
    
    context = {
        'titulo_pagina': 'Belezas da Natureza',
        'pontos_geojson': pontos_geojson,
        'tem_pontos': pontos.exists(),
        'breadcrumbs': breadcrumbs,
        'categorias_filtros': categorias_filtros
    }
    return render(request, 'gerenciamento_destino/html/mapa_interativo.html', context)

def cultura_e_tradicoes_view(request):
    pontos = PontoDeInteresse.objects.filter(publicado=True, categoria__grupo='CULTURA')
    categorias_filtros = Categoria.objects.filter(grupo='CULTURA')

    breadcrumbs = [
        {'nome': 'Início', 'url': reverse('gerenciamento_home:home')},
        {'nome': 'Destino Roraima', 'url': reverse('destino:pagina_inicial')},
        {'nome': 'Cultura e Tradições', 'url': ''},
    ]

    pontos_geojson = {"type": "FeatureCollection", "features": [
        {"type": "Feature", 
         "geometry": {"type": "Point", "coordinates": [float(str(p.longitude).replace(',', '.')), float(str(p.latitude).replace(',', '.'))]},
         "properties": {
             "titulo": p.titulo, "descricao_curta": p.descricao_curta, 
             "imagem_url": p.imagem_principal.url if p.imagem_principal else '', 
             "detalhe_url": reverse('destino:detalhe_ponto', args=[p.slug]), 
             "slug": p.slug,
             "categoria_slug": p.categoria.slug,
             "icone_url": p.categoria.icone.url if p.categoria.icone else None
            }
        } for p in pontos]}
    
    context = {
        'titulo_pagina': 'Cultura e Tradições',
        'pontos_geojson': pontos_geojson,
        'tem_pontos': pontos.exists(),
        'breadcrumbs': breadcrumbs,
        'categorias_filtros': categorias_filtros
    }
    return render(request, 'gerenciamento_destino/html/mapa_interativo.html', context)

def lista_roteiros_view(request):
    roteiros = Roteiro.objects.filter(publicado=True).order_by('titulo')
    
    breadcrumbs = [
        {'nome': 'Início', 'url': reverse('gerenciamento_home:home')},
        {'nome': 'Destino Roraima', 'url': reverse('destino:pagina_inicial')},
        {'nome': 'Roteiros Temáticos', 'url': ''},
    ]

    context = {
        'roteiros': roteiros,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'gerenciamento_destino/html/lista_roteiros.html', context)