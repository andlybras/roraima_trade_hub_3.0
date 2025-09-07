from django.shortcuts import render, get_object_or_404
from .models import ConteudoInteligencia, Grafico # Adicione Grafico
import re # Adicione o import para Expressões Regulares

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

    # Lógica para substituir as tags de gráfico pelo código JS
    def substituir_grafico(match):
        chave = match.group(1)
        try:
            grafico = Grafico.objects.get(chave=chave)
            container_id = f"grafico-container-{grafico.chave}"
            script_grafico = f"""
                <div id='{container_id}' style='width: 100%; height: 400px; margin: 20px 0;'></div>
                <script type='text/javascript'>
                    var chartDom = document.getElementById('{container_id}');
                    var myChart = echarts.init(chartDom);
                    var option = {grafico.codigo_js_echarts};
                    myChart.setOption(option);
                </script>
            """
            return script_grafico
        except Grafico.DoesNotExist:
            return f"<p style='color: red;'>[Gráfico com a chave '{chave}' não encontrado.]</p>"

    corpo_processado = re.sub(r'\[grafico:([\w-]+)\]', substituir_grafico, conteudo.corpo_conteudo)

    context = {
        'conteudo': conteudo,
        'corpo_processado': corpo_processado,
    }
    return render(request, 'gerenciamento_inteligencia_mercado/html/detalhe_conteudo.html', context)