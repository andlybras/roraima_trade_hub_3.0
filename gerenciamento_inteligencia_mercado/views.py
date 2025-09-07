from django.shortcuts import render, get_object_or_404
from .models import ConteudoInteligencia, Grafico, TermoGlossario # Adicione Grafico
import re # Adicione o import para Expressões Regulares
import json

def pagina_inicial_inteligencia(request):
    """
    Renderiza a página inicial do módulo de Inteligência de Mercado,
    que serve como um painel de navegação e exibe um gráfico principal.
    """
    # Apenas busca o objeto do gráfico e o envia para o template
    grafico_principal = Grafico.objects.filter(is_grafico_principal=True).first()

    context = {
        'grafico_principal': grafico_principal,
    }
    return render(request, 'gerenciamento_inteligencia_mercado/html/pagina_inicial.html', context)


def lista_conteudo_por_categoria(request, categoria):
    """
    Filtra e exibe todos os conteúdos de uma categoria específica.
    """
    # Pega o nome "bonito" da categoria (ex: "Dados Estruturais")
    categoria_verbose = dict(ConteudoInteligencia.CATEGORIAS).get(categoria)

    # Busca os cards daquela categoria no banco de dados
    cards = ConteudoInteligencia.objects.filter(categoria=categoria).order_by('titulo_card')

    context = {
        'categoria_verbose': categoria_verbose,
        'cards': cards,
    }
    return render(request, 'gerenciamento_inteligencia_mercado/html/lista_cards.html', context)

def detalhe_conteudo(request, pk):
    conteudo = get_object_or_404(ConteudoInteligencia, pk=pk)
    
    # LÓGICA REFEITA: Agora ela só cria a DIV com os dados
    def substituir_grafico(match):
        chave = match.group(1)
        try:
            grafico = Grafico.objects.get(chave=chave)
            container_id = f"grafico-container-{grafico.chave}"
            
            # Converte o código do gráfico para uma string JSON segura para HTML
            # Usamos json.dumps para garantir que aspas e outros caracteres sejam tratados
            # O código no admin deve ser apenas o objeto {...}, sem 'option = '
            chart_options_json = json.dumps(json.loads(grafico.codigo_js_echarts))

            # Retorna apenas a DIV, com os dados do gráfico em um atributo 'data-options'
            html_grafico = f"""
                <div id='{container_id}' 
                     class='echarts-container' 
                     style='width: 100%; height: 400px; margin: 20px 0;'
                     data-options='{chart_options_json}'>
                </div>
            """
            return html_grafico
            
        except Grafico.DoesNotExist:
            return f"<p style='color: red;'>[Gráfico com a chave '{chave}' não encontrado.]</p>"
        except json.JSONDecodeError:
            return f"<p style='color: red;'>[Erro de sintaxe no código do gráfico '{chave}'. Verifique o JSON no admin.]</p>"

    corpo_processado = re.sub(r'\[grafico:([\w-]+)\]', substituir_grafico, conteudo.corpo_conteudo)

    context = {
        'conteudo': conteudo,
        'corpo_processado': corpo_processado,
    }
    return render(request, 'gerenciamento_inteligencia_mercado/html/detalhe_conteudo.html', context)

# Arquivo: gerenciamento_inteligencia_mercado/views.py

# ... (outras views como pagina_inicial_inteligencia, etc.) ...

def glossario_view(request):
    """
    Busca todos os termos do glossário e os agrupa pela letra inicial.
    """
    termos_ordenados = TermoGlossario.objects.order_by('termo')
    termos_agrupados = {}

    for termo in termos_ordenados:
        letra_inicial = termo.termo[0].upper()
        if letra_inicial not in termos_agrupados:
            termos_agrupados[letra_inicial] = []
        termos_agrupados[letra_inicial].append(termo)

    context = {
        'termos_agrupados': termos_agrupados,
        'titulo_pagina': 'Glossário de Termos' # CORREÇÃO: Adiciona o título ao contexto
    }
    return render(request, 'gerenciamento_inteligencia_mercado/html/glossario.html', context)