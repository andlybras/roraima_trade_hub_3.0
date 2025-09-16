from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from .models import ConteudoApresentacaoVender, PerguntaFrequente, PerguntaUsuario, DadosEmpresariais
from .forms import DadosEmpresaForm, DadosResponsavelForm, DadosComplementaresForm, UserRegistrationForm, UserLoginForm, ResendActivationEmailForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.db.models import Q
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
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
    else:
        form = UserRegistrationForm()

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

@login_required
def dashboard_view(request):
    return render(request, 'gerenciamento_vender/html/dashboard.html')

@login_required
def dashboard_visao_geral(request):
    dados_empresa, created = DadosEmpresariais.objects.get_or_create(usuario=request.user)
    status_reg_display = dict(DadosEmpresariais.STATUS_CHOICES).get(dados_empresa.status)
    status_vit = 'INATIVA'
    status_vit_display = {'PÚBLICA': 'VITRINE PÚBLICA', 'INATIVA': 'VITRINE INATIVA'}.get(status_vit, 'INDEFINIDO')
    context = {
        'status_registro': dados_empresa.status,
        'status_registro_display': status_reg_display,
        'status_vitrine': status_vit,
        'status_vitrine_display': status_vit_display,
        'selos': [
            {'nome': 'Empresa Roraimense', 'icone': 'gerenciamento_vender/icons/selo-roraimense.svg', 'conquistado': True},
            {'nome': 'Pronta para Exportar', 'icone': 'gerenciamento_vender/icons/selo-exportador.svg', 'conquistado': True},
            {'nome': 'Selo Verde', 'icone': 'gerenciamento_vender/icons/selo-roraimense.svg', 'conquistado': False},
        ],
        'notificacoes': ['Bem-vindo(a) ao seu painel!', 'Para começar, preencha seus dados empresariais.'],
        'historico': [f"{dados_empresa.data_criacao.strftime('%d/%m/%Y')} - Conta criada."]
    }
    return render(request, 'gerenciamento_vender/html/dashboard_partials/visao_geral.html', context)

@login_required
def dashboard_dados_empresariais(request):
    dados_empresa, created = DadosEmpresariais.objects.get_or_create(usuario=request.user)
    request.session['cadastro_id'] = dados_empresa.id
    return redirect('vender:dados_empresariais_form', etapa=1)

@login_required
def dados_empresariais_form_view(request, etapa):
    forms = { 1: DadosEmpresaForm, 2: DadosResponsavelForm, 3: DadosComplementaresForm }
    form_class = forms.get(etapa)
    cadastro_id = request.session.get('cadastro_id')
    if not cadastro_id:
        return redirect('vender:dashboard_dados_empresariais')
    cadastro = get_object_or_404(DadosEmpresariais, id=cadastro_id, usuario=request.user) # Mais segurança
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

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def form_valid(self, form):
        # Pega o usuário antes que a senha seja alterada
        user = form.user
        
        # Chama a função original do Django para alterar a senha e obter a resposta
        response = super().form_valid(form)
        
        # Agora, envia o e-mail de notificação
        mail_subject = 'Sua senha no Roraima Trade Hub foi alterada'
        message = render_to_string('gerenciamento_vender/html/emails/password_change_notification_email.html')
        send_mail(mail_subject, message, 'nao-responda@roraimatradehub.com', [user.email])
        
        return response
    
def reenviar_ativacao_view(request):
    if request.method == 'POST':
        form = ResendActivationEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                if not user.is_active:
                    # Lógica de envio de e-mail (reutilizada do cadastro)
                    current_site = get_current_site(request)
                    mail_subject = 'Ative sua conta no Roraima Trade Hub.'
                    message = render_to_string('gerenciamento_vender/html/emails/confirmacao_cadastro_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
                    send_mail(mail_subject, message, 'nao-responda@roraimatradehub.com', [email])
            except User.DoesNotExist:
                # Se o usuário não existe, não fazemos nada, mas fingimos que deu certo
                # Isso é uma medida de segurança para não revelar quais e-mails estão cadastrados
                pass
            return redirect('vender:reenviar_ativacao_enviado')
    else:
        form = ResendActivationEmailForm()
    
    return render(request, 'gerenciamento_vender/html/reenviar_ativacao_form.html', {'form': form})

def reenviar_ativacao_enviado_view(request):
    return render(request, 'gerenciamento_vender/html/reenviar_ativacao_enviado.html')