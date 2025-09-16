from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import ConteudoApresentacaoVender, PerguntaFrequente, PerguntaUsuario, DadosEmpresariais
from .forms import DadosEmpresaForm, DadosResponsavelForm, DadosComplementaresForm
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
    return render(request, 'gerenciamento_vender/html/dashboard.html')

def dashboard_visao_geral(request):
    # (código existente da Visão Geral, sem alterações)
    status_reg = 'PENDENTE'
    status_vit = 'INATIVA'
    status_reg_display = {'ATIVO': 'REGISTRO ATIVO', 'PENDENTE': 'PENDENTE DE DADOS', 'ANALISE': 'EM ANÁLISE'}.get(status_reg, 'INDEFINIDO')
    status_vit_display = {'PÚBLICA': 'VITRINE PÚBLICA', 'INATIVA': 'VITRINE INATIVA'}.get(status_vit, 'INDEFINIDO')
    context = { 'status_registro': status_reg, 'status_registro_display': status_reg_display, 'status_vitrine': status_vit, 'status_vitrine_display': status_vit_display, 'selos': [{'nome': 'Empresa Roraimense', 'icone': 'gerenciamento_vender/icons/selo-roraimense.svg', 'conquistado': True}, {'nome': 'Pronta para Exportar', 'icone': 'gerenciamento_vender/icons/selo-exportador.svg', 'conquistado': True}, {'nome': 'Selo Verde', 'icone': 'gerenciamento_vender/icons/selo-roraimense.svg', 'conquistado': False}], 'notificacoes': ['Sua vitrine foi publicada com sucesso!', 'Um novo documento de suporte foi adicionado.', 'Seu registro foi ativado em 14/09/2025.'], 'historico': ['15/09/2025 - Vitrine publicada.', '14/09/2025 - Registro da empresa ativado.', '12/09/2025 - Dados empresariais enviados para análise.', '10/09/2025 - Conta criada.']}
    return render(request, 'gerenciamento_vender/html/dashboard_partials/visao_geral.html', context)


def dashboard_dados_empresariais(request):
    # Lógica inicial: Tenta encontrar um cadastro em andamento ou cria um novo "rascunho".
    # No futuro, isso será ligado ao `request.user`. Por enquanto, criamos um novo a cada vez.
    cadastro_rascunho = DadosEmpresariais.objects.create()
    request.session['cadastro_id'] = cadastro_rascunho.id
    
    return redirect('vender:dados_empresariais_form', etapa=1)


# Em gerenciamento_vender/views.py

def dados_empresariais_form_view(request, etapa):
    forms = { 1: DadosEmpresaForm, 2: DadosResponsavelForm, 3: DadosComplementaresForm }
    form_class = forms.get(etapa)
    
    cadastro_id = request.session.get('cadastro_id')
    if not cadastro_id:
        return redirect('vender:dashboard_dados_empresariais')
        
    cadastro = get_object_or_404(DadosEmpresariais, id=cadastro_id)

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=cadastro)
        if form.is_valid():
            form.save()

            proxima_etapa = etapa + 1
            if proxima_etapa > len(forms):
                # Finalizou a última etapa
                cadastro.status = 'EM_ANALISE'
                cadastro.save()
                del request.session['cadastro_id']
                # Retorna o template de sucesso para o AJAX
                return render(request, 'gerenciamento_vender/html/dashboard_partials/dados_empresariais_sucesso.html')
            else:
                # Prepara o formulário da PRÓXIMA etapa para o AJAX
                proximo_form = forms.get(proxima_etapa)(instance=cadastro)
                context = {
                    'form': proximo_form,
                    'etapa': proxima_etapa,
                    'total_etapas': len(forms),
                }
                return render(request, 'gerenciamento_vender/html/dashboard_partials/dados_empresariais_form.html', context)
    else:
        # GET request: Mostra o formulário da etapa atual
        form = form_class(instance=cadastro)

    context = {
        'form': form,
        'etapa': etapa,
        'total_etapas': len(forms),
    }
    # Retorna o template da ETAPA ATUAL para o AJAX
    return render(request, 'gerenciamento_vender/html/dashboard_partials/dados_empresariais_form.html', context)

def criar_perfil_empresarial_view(request):
    return HttpResponse("<h1>Página para Criação de Perfil Empresarial (Em Construção)</h1>")
