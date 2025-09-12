from django.shortcuts import render, get_object_or_404
from .models import ConteudoInteligencia, Grafico, TermoGlossario
import re
import json

def pagina_inicial_inteligencia(request):
    grafico_principal = Grafico.objects.filter(is_grafico_principal=True).first()
    context = {
        'grafico_principal': grafico_principal,
    }
    return render(request, 'gerenciamento_inteligencia_mercado/html/pagina_inicial.html', context)

def lista_conteudo_por_categoria(request, categoria):
    categoria_verbose = dict(ConteudoInteligencia.CATEGORIAS).get(categoria)
    cards = ConteudoInteligencia.objects.filter(
        categoria=categoria,
        publicado=True
    ).order_by('titulo_card')
    context = {
        'categoria_verbose': categoria_verbose,
        'cards': cards,
        'categoria': categoria,
    }
    return render(request, 'gerenciamento_inteligencia_mercado/html/lista_cards.html', context)

def detalhe_conteudo(request, pk):
    conteudo = get_object_or_404(ConteudoInteligencia, pk=pk, publicado=True)

    def substituir_grafico(match):
        chave = match.group(1)
        try:
            grafico = Grafico.objects.get(chave=chave)
            if grafico.tipo_grafico == 'OPTION_SIMPLE':
                container_id = f"grafico-container-{grafico.chave}"
                try:
                    chart_options_json = json.dumps(json.loads(grafico.codigo_js_echarts))
                    html_grafico = f"""
                        <div id='{container_id}' 
                             class='echarts-container' 
                             style='width: 100%; height: 400px; margin: 20px 0;'
                             data-options='{chart_options_json}'>
                        </div>"""
                    return html_grafico
                except json.JSONDecodeError:
                    return f"<p style='color: red;'>[Erro de sintaxe no código do gráfico '{chave}'. Verifique o JSON no admin.]</p>"
            elif grafico.tipo_grafico == 'SCRIPT_COMPLETO':
                 return f"<div class='script-grafico-wrapper'>{grafico.codigo_js_echarts}</div>"
        except Grafico.DoesNotExist:
            return f"<p style='color: red;'>[Gráfico com a chave '{chave}' não encontrado.]</p>"

    corpo_processado = re.sub(r'\[grafico:([\w-]+)\]', substituir_grafico, conteudo.corpo_conteudo)
    
    context = {
        'conteudo': conteudo,
        'corpo_processado': corpo_processado,
    }
    return render(request, 'gerenciamento_inteligencia_mercado/html/detalhe_conteudo.html', context)

def glossario_view(request):
    termos_ordenados = TermoGlossario.objects.order_by('termo')
    termos_agrupados = {}
    for termo in termos_ordenados:
        letra_inicial = termo.termo[0].upper()
        if letra_inicial not in termos_agrupados:
            termos_agrupados[letra_inicial] = []
        termos_agrupados[letra_inicial].append(termo)
    
    context = {
        'termos_agrupados': termos_agrupados,
        'titulo_pagina': 'Glossário' 
    }
    return render(request, 'gerenciamento_inteligencia_mercado/html/glossario.html', context)

def grafico_preview_view(request, pk):
    grafico = get_object_or_404(Grafico, pk=pk)
    context = {
        'grafico': grafico,
    }
    return render(request, 'gerenciamento_inteligencia_mercado/html/grafico_previews.html', context)