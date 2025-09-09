# Arquivo: gerenciamento_registros/views.py

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
# Imports corrigidos e completos
from .forms import (
    EmpresaEmpreendedorRegistrationForm, AprendizRegistrationForm, 
    ResendActivationEmailForm, EmpresaProfileForm, EmpreendedorProfileForm
)
from .models import CustomUser, EmpresaProfile, EmpreendedorProfile, AprendizProfile
from .tokens import account_activation_token
from django.contrib import messages
from django.contrib.auth.decorators import login_required # Import do protetor de login

class BaseRegisterView(CreateView):
    model = CustomUser
    success_url = reverse_lazy('gerenciamento_registros:ativacao_enviada')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        subject = 'Ative sua conta no Roraima Trade Hub'
        message = render_to_string('gerenciamento_registros/emails/ativacao_conta_email.html', {
            'user': user,
            'protocol': 'http',
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)
        return redirect(self.success_url)

class EmpresaEmpreendedorRegisterView(BaseRegisterView):
    form_class = EmpresaEmpreendedorRegistrationForm
    template_name = 'gerenciamento_registros/html/registro_empresa_empreendedor.html'

class AprendizRegisterView(BaseRegisterView):
    form_class = AprendizRegistrationForm
    template_name = 'gerenciamento_registros/html/registro_aprendiz.html'

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        
        # --- LÓGICA DE CRIAÇÃO DE PERFIL ADICIONADA ---
        if user.tipo_usuario == 'EMPREENDEDOR':
            EmpreendedorProfile.objects.get_or_create(user=user)
        elif user.tipo_usuario == 'EMPRESA':
            EmpresaProfile.objects.get_or_create(user=user)
        
        return redirect('gerenciamento_registros:ativacao_sucesso')
    else:
        return redirect('gerenciamento_registros:ativacao_invalida')
    
# Em gerenciamento_registros/views.py

def resend_activation_email_view(request):
    if request.method == 'POST':
        form = ResendActivationEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                if not user.is_active:
                    # Reutiliza a lógica de envio de e-mail
                    current_site = get_current_site(request)
                    subject = 'Ative sua conta no Roraima Trade Hub'
                    message = render_to_string('gerenciamento_registros/emails/ativacao_conta_email.html', {
                        'user': user,
                        'protocol': 'http',
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
                    user.email_user(subject, message)
                    # Redireciona para a mesma página de sucesso do registro
                    return redirect('gerenciamento_registros:ativacao_enviada')
                else:
                    # Se o usuário já estiver ativo, informa e manda pro login
                    messages.info(request, 'Esta conta já está ativa. Por favor, faça o login.')
                    return redirect('gerenciamento_registros:login')
            except CustomUser.DoesNotExist:
                # Se o e-mail não existe, redireciona para a mesma página de sucesso
                # para não confirmar se um e-mail está ou não no sistema (medida de segurança).
                return redirect('gerenciamento_registros:ativacao_enviada')
    else:
        form = ResendActivationEmailForm()

    return render(request, 'gerenciamento_registros/html/resend_activation_form.html', {'form': form})

# --- DECORATOR @login_required ADICIONADO ---
@login_required
def perfil_update_view(request):
    user_type = request.user.tipo_usuario
    template_name = ''
    form_class = None
    profile_model = None

    if user_type == 'EMPRESA':
        template_name = 'gerenciamento_registros/html/perfil_empresa.html'
        form_class = EmpresaProfileForm
        profile_model = EmpresaProfile
    elif user_type == 'EMPREENDEDOR':
        template_name = 'gerenciamento_registros/html/perfil_empreendedor.html'
        form_class = EmpreendedorProfileForm
        profile_model = EmpreendedorProfile
    else:
        # Se o usuário logado for de outro tipo (ex: Aprendiz), redireciona para o dashboard principal
        return redirect('vender:dashboard')

    profile, created = profile_model.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('vender:dashboard')
    else:
        form = form_class(instance=profile)

    return render(request, template_name, {'form': form})