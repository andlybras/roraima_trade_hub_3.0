# gerenciamento_vender/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User 
from .models import ConteudoApresentacaoVender, PerguntaFrequente, PerguntaUsuario, DadosEmpresariais
from .forms import DadosEmpresaForm, DadosResponsavelForm, DadosComplementaresForm, UserRegistrationForm
from django.db.models import Q
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string # Importado apenas uma vez
from .tokens import account_activation_token

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
            link_resposta = request.build_absolute_uri(reverse('vender:ver_resposta', args=[nova_pergunta.identificador_unico]))
            contexto_email = {'pergunta': nova_pergunta, 'link_resposta': link_resposta}
            corpo_email = render_to_string('gerenciamento_vender/html/emails/confirmacao_pergunta.txt', contexto_email)
            send_mail('Sua pergunta foi recebida - Roraima Trade Hub', corpo_email, 'nao-responda@roraimatradehub.com', [email], fail_silently=False)
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

def cadastro_sucesso_view(request):
    return render(request, 'gerenciamento_vender/html/cadastro_sucesso.html')

# --- FUNÇÃO CORRIGIDA ---
def criar_perfil_empresarial_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            novo_usuario = User.objects.create_user(
                username=cd['email'],
                email=cd['email'],
                password=cd['password']
            )
            novo_usuario.is_active = False
            novo_usuario.save()

            current_site = get_current_site(request)
            mail_subject = 'Ative sua conta no Roraima Trade Hub.'
            message = render_to_string('gerenciamento_vender/html/emails/confirmacao_cadastro_email.html', {
                'user': novo_usuario,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(novo_usuario.pk)),
                'token': account_activation_token.make_token(novo_usuario),
            })
            send_mail(mail_subject, message, 'nao-responda@roraimatradehub.com', [cd['email']])
            
            DadosEmpresariais.objects.create(usuario=novo_usuario)
            return redirect('vender:cadastro_sucesso')
        # Se o formulário NÃO for válido, a função continua e renderiza o template com o formulário preenchido e os erros
    else:
        form = UserRegistrationForm()
        
    # Esta linha agora é executada para GET requests E para POST requests inválidos
    return render(request, 'gerenciamento_vender/html/cadastro.html', {'form': form})

def ativar_conta_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'gerenciamento_vender/html/ativacao_sucesso.html')
    else:
        return render(request, 'gerenciamento_vender/html/ativacao_invalida.html')

def acessar_ambiente_empresarial_view(request):
    return HttpResponse("<h1>Página de Acesso ao Ambiente Empresarial (Em Construção)</h1>")

def dashboard_view(request):
    return render(request, 'gerenciamento_vender/html/dashboard.html')

def dashboard_visao_geral(request):
    # ... (código existente da Visão Geral) ...
    status_reg = 'PENDENTE'
    status_vit = 'INATIVA'
    status_reg_display = {'ATIVO': 'REGISTRO ATIVO', 'PENDENTE': 'PENDENTE DE DADOS', 'ANALISE': 'EM ANÁLISE'}.get(status_reg, 'INDEFINIDO')
    status_vit_display = {'PÚBLICA': 'VITRINE PÚBLICA', 'INATIVA': 'VITRINE INATIVA'}.get(status_vit, 'INDEFINIDO')
    context = { 'status_registro': status_reg, 'status_registro_display': status_reg_display, 'status_vitrine': status_vit, 'status_vitrine_display': status_vit_display, 'selos': [{'nome': 'Empresa Roraimense', 'icone': 'gerenciamento_vender/icons/selo-roraimense.svg', 'conquistado': True}, {'nome': 'Pronta para Exportar', 'icone': 'gerenciamento_vender/icons/selo-exportador.svg', 'conquistado': True}, {'nome': 'Selo Verde', 'icone': 'gerenciamento_vender/icons/selo-roraimense.svg', 'conquistado': False}], 'notificacoes': ['Sua vitrine foi publicada com sucesso!', 'Um novo documento de suporte foi adicionado.', 'Seu registro foi ativado em 14/09/2025.'], 'historico': ['15/09/2025 - Vitrine publicada.', '14/09/2025 - Registro da empresa ativado.', '12/09/2025 - Dados empresariais enviados para análise.', '10/09/2025 - Conta criada.']}
    return render(request, 'gerenciamento_vender/html/dashboard_partials/visao_geral.html', context)

def dashboard_dados_empresariais(request):
    # ... (código existente) ...
    cadastro_rascunho = DadosEmpresariais.objects.create()
    request.session['cadastro_id'] = cadastro_rascunho.id
    return redirect('vender:dados_empresariais_form', etapa=1)

def dados_empresariais_form_view(request, etapa):
    # ... (código existente) ...
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
                cadastro.status = 'EM_ANALISE'
                cadastro.save()
                del request.session['cadastro_id']
                return render(request, 'gerenciamento_vender/html/dashboard_partials/dados_empresariais_sucesso.html')
            else:
                proximo_form = forms.get(proxima_etapa)(instance=cadastro)
                context = {'form': proximo_form, 'etapa': proxima_etapa, 'total_etapas': len(forms)}
                return render(request, 'gerenciamento_vender/html/dashboard_partials/dados_empresariais_form.html', context)
    else:
        form = form_class(instance=cadastro)
    context = {'form': form, 'etapa': etapa, 'total_etapas': len(forms)}
    return render(request, 'gerenciamento_vender/html/dashboard_partials/dados_empresariais_form.html', context)