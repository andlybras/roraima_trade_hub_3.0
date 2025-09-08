from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from .forms import EmpresaEmpreendedorRegistrationForm, AprendizRegistrationForm
from .models import CustomUser
from .tokens import account_activation_token

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
        return redirect('gerenciamento_registros:ativacao_sucesso')
    else:
        return redirect('gerenciamento_registros:ativacao_invalida')