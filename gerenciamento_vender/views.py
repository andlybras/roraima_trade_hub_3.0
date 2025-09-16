# gerenciamento_vender/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import ConteudoApresentacaoVender, PerguntaFrequente, PerguntaUsuario
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

def pagina_inicial_vender(request):
    conteudo_ativo = ConteudoApresentacaoVender.objects.filter(em_exibicao=True).first()
    context = { 'conteudo_apresentacao': conteudo_ativo, }
    return render(request, 'gerenciamento_vender/html/pagina_inicial_vender.html', context)

def faq_view(request):
    query = request.GET.get('q', '') 
    lista_perguntas = PerguntaFrequente.objects.filter(publicada=True)
    if query:
        lista_perguntas = lista_perguntas.filter(Q(pergunta__icontains=query) | Q(resposta__icontains=query))
    perguntas_agrupadas = {}
    for pergunta in lista_perguntas:
        letra_inicial = pergunta.pergunta[0].upper()
        if letra_inicial not in perguntas_agrupadas:
            perguntas_agrupadas[letra_inicial] = []
        perguntas_agrupadas[letra_inicial].append(pergunta)
    context = {
        'titulo_pagina': 'Perguntas Frequentes',
        'perguntas_agrupadas': perguntas_agrupadas,
        'query': query,
        'total_resultados': lista_perguntas.count()
    }
    return render(request, 'gerenciamento_vender/html/faq.html', context)

def submeter_pergunta_view(request):
    if request.method == 'POST':
        email = request.POST.get('email_usuario')
        pergunta_texto = request.POST.get('pergunta_usuario')

        if email and pergunta_texto:
            nova_pergunta = PerguntaUsuario.objects.create(email_usuario=email, pergunta=pergunta_texto)
            
            # Enviar e-mail de confirmação
            link_resposta = request.build_absolute_uri(reverse('vender:ver_resposta', args=[nova_pergunta.identificador_unico]))
            contexto_email = {'pergunta': nova_pergunta, 'link_resposta': link_resposta}
            
            corpo_email = render_to_string('gerenciamento_vender/html/emails/confirmacao_pergunta.txt', contexto_email)
            
            send_mail(
                'Sua pergunta foi recebida - Roraima Trade Hub',
                corpo_email,
                'nao-responda@roraimatradehub.com',
                [email],
                fail_silently=False,
            )

            return redirect('vender:submissao_sucesso')
    
    return redirect('vender:faq')

def submissao_sucesso_view(request):
    return render(request, 'gerenciamento_vender/html/submissao_sucesso.html')

def ver_resposta_view(request, identificador):
    pergunta = get_object_or_404(PerguntaUsuario, identificador_unico=identificador)

    if request.method == 'POST':
        avaliacao = request.POST.get('avaliacao')
        if avaliacao == 'util':
            pergunta.resposta_foi_util = True
        elif avaliacao == 'nao_util':
            pergunta.resposta_foi_util = False
        pergunta.save()

    context = {'pergunta': pergunta}
    return render(request, 'gerenciamento_vender/html/resposta_privada.html', context)


def criar_perfil_empresarial_view(request):
    return HttpResponse("<h1>Página para Criação de Perfil Empresarial (Em Construção)</h1>")

def acessar_ambiente_empresarial_view(request):
    return HttpResponse("<h1>Página de Acesso ao Ambiente Empresarial (Em Construção)</h1>")

# Adicione estas novas funções no final de gerenciamento_vender/views.py

def dashboard_view(request):
    """
    Renderiza a "casca" principal do dashboard.
    """
    return render(request, 'gerenciamento_vender/html/dashboard.html')

# Em gerenciamento_vender/views.py, substitua a função dashboard_visao_geral

def dashboard_visao_geral(request):
    """
    Renderiza APENAS o conteúdo da aba "Visão Geral" com dados provisórios.
    """
    # Estes dados são provisórios. No futuro, virão do banco de dados.
    context = {
        'status_registro': 'ATIVO', # Mude para 'PENDENTE' ou 'ANALISE' para testar
        'status_vitrine': 'PÚBLICA', # Mude para 'INATIVA' para testar
        'selos': [
            {'nome': 'Empresa Roraimense', 'icone': 'gerenciamento_vender/icons/selo-roraimense.svg', 'conquistado': True},
            {'nome': 'Pronta para Exportar', 'icone': 'gerenciamento_vender/icons/selo-exportador.svg', 'conquistado': True},
            {'nome': 'Selo Verde', 'icone': 'gerenciamento_vender/icons/selo-roraimense.svg', 'conquistado': False},
        ],
        'notificacoes': [
            'Sua vitrine foi publicada com sucesso!',
            'Um novo documento de suporte foi adicionado.',
            'Seu registro foi ativado em 14/09/2025.'
        ],
        'historico': [
            '15/09/2025 - Vitrine publicada.',
            '14/09/2025 - Registro da empresa ativado.',
            '12/09/2025 - Dados empresariais enviados para análise.',
            '10/09/2025 - Conta criada.',
        ]
    }
    return render(request, 'gerenciamento_vender/html/dashboard_partials/visao_geral.html', context)

def dashboard_dados_empresariais(request):
    """
    Renderiza APENAS o conteúdo da aba "Dados Empresariais".
    """
    # Por enquanto, podemos reutilizar um template genérico
    return render(request, 'gerenciamento_vender/html/dashboard_partials/em_construcao.html', {'aba': 'Dados Empresariais'})

# Restante do seu arquivo views.py...
# ...