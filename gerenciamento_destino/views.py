# gerenciamento_destino/views.py
# (Código completo com a adição do 'slug' nas propriedades do GeoJSON)

from django.shortcuts import render, get_object_or_404
from .models import ConteudoApresentacaoDestino, Categoria, PontoDeInteresse
from django.urls import reverse

def pagina_inicial_destino(request):
    conteudo_ativo = ConteudoApresentacaoDestino.objects.filter(em_exibicao=True).first()
    context = {'conteudo_apresentacao': conteudo_ativo}
    return render(request, 'gerenciamento_destino/html/pagina_inicial_destino.html', context)

def belezas_da_natureza_view(request):
    pontos = PontoDeInteresse.objects.filter(publicado=True, categoria__grupo='NATUREZA')
    breadcrumbs = [{'nome': 'Início', 'url': reverse('gerenciamento_home:home')},{'nome': 'Destino Roraima', 'url': reverse('destino:pagina_inicial')},{'nome': 'Belezas da Natureza', 'url': ''}]
    pontos_geojson = {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [float(str(p.longitude).replace(',', '.')), float(str(p.latitude).replace(',', '.'))]}, "properties": {"titulo": p.titulo, "descricao_curta": p.descricao_curta, "imagem_url": p.imagem_principal.url if p.imagem_principal else '', "detalhe_url": reverse('destino:detalhe_ponto', args=[p.slug]), "slug": p.slug}} for p in pontos]}
    context = {'titulo_pagina': 'Belezas da Natureza', 'pontos_geojson': pontos_geojson, 'tem_pontos': pontos.exists(), 'breadcrumbs': breadcrumbs}
    return render(request, 'gerenciamento_destino/html/mapa_interativo.html', context)

def cultura_e_tradicoes_view(request):
    pontos = PontoDeInteresse.objects.filter(publicado=True, categoria__grupo='CULTURA')
    breadcrumbs = [{'nome': 'Início', 'url': reverse('gerenciamento_home:home')},{'nome': 'Destino Roraima', 'url': reverse('destino:pagina_inicial')},{'nome': 'Cultura e Tradições', 'url': ''}]
    pontos_geojson = {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [float(str(p.longitude).replace(',', '.')), float(str(p.latitude).replace(',', '.'))]}, "properties": {"titulo": p.titulo, "descricao_curta": p.descricao_curta, "imagem_url": p.imagem_principal.url if p.imagem_principal else '', "detalhe_url": reverse('destino:detalhe_ponto', args=[p.slug]), "slug": p.slug}} for p in pontos]}
    context = {'titulo_pagina': 'Cultura e Tradições', 'pontos_geojson': pontos_geojson, 'tem_pontos': pontos.exists(), 'breadcrumbs': breadcrumbs}
    return render(request, 'gerenciamento_destino/html/mapa_interativo.html', context)

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