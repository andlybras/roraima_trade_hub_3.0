from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# ADICIONADO IMPORTS QUE FALTAVAM
from .models import CustomUser, AprendizProfile, EmpreendedorProfile, EmpresaProfile 
from django_recaptcha.fields import ReCaptchaField
from django.core.exceptions import ValidationError

class EmpresaEmpreendedorRegistrationForm(UserCreationForm):
    tipo_perfil = forms.ChoiceField(
        choices=[('EMPRESA', 'Sou uma Empresa'), ('EMPREENDEDOR', 'Sou um Empreendedor')],
        widget=forms.RadioSelect, 
        label="Este perfil é para:",
        required=True
    )
    email = forms.EmailField(required=True, help_text="O e-mail deve ser único.", label="E-mail")
    email2 = forms.EmailField(label="Confirme seu e-mail")
    captcha = ReCaptchaField()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'tipo_perfil', 'email')

    def clean_email2(self):
        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        if email and email2 and email != email2:
            raise ValidationError("Os e-mails não são iguais.", code='email_mismatch')
        return email2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo_usuario = self.cleaned_data['tipo_perfil']
        if commit:
            user.save()
        return user

class AprendizRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="Nome Completo")
    email = forms.EmailField(required=True, help_text="O e-mail deve ser único.", label="E-mail")
    email2 = forms.EmailField(label="Confirme seu e-mail")
    cpf = forms.CharField(required=True, label="CPF")
    data_nascimento = forms.DateField(required=True, label="Data de Nascimento", widget=forms.DateInput(attrs={'type': 'date'}))
    residencia = forms.CharField(required=True, label="Estado/País de Residência")
    nivel_conhecimento_comex = forms.ChoiceField(
        choices=AprendizProfile.NIVEL_CONHECIMENTO_CHOICES,
        label="Nível de conhecimento em Comércio Exterior"
    )
    captcha = ReCaptchaField()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'email', 'email2')

    def clean_email2(self):
        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        if email and email2 and email != email2:
            raise ValidationError("Os e-mails não são iguais.", code='email_mismatch')
        return email2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.tipo_usuario = 'APRENDIZ'
        if commit:
            user.save()
            AprendizProfile.objects.create(
                user=user,
                cpf=self.cleaned_data.get('cpf'),
                data_nascimento=self.cleaned_data.get('data_nascimento'),
                residencia=self.cleaned_data.get('residencia'),
                nivel_conhecimento_comex=self.cleaned_data.get('nivel_conhecimento_comex'),
            )
        return user
    
class PublicAuthenticationForm(AuthenticationForm):

    def confirm_login_allowed(self, user):
        if user.is_staff:
            raise ValidationError(
                "Contas administrativas devem acessar pelo painel de administração.",
                code='admin_login_denied'
            )
        super().confirm_login_allowed(user)
        
class ResendActivationEmailForm(forms.Form):
    email = forms.EmailField(label="E-mail", widget=forms.TextInput(attrs={'placeholder': 'Digite o e-mail cadastrado'}))
    
class EmpreendedorProfileForm(forms.ModelForm):
    class Meta:
        model = EmpreendedorProfile
        fields = ['nome_completo', 'cpf'] # Campos do Empreendedor
        # Adicione widgets se precisar de máscaras (ex: CPF)

class EmpresaProfileForm(forms.ModelForm):
    class Meta:
        model = EmpresaProfile
        fields = ['nome_fantasia', 'razao_social', 'cnpj'] # Campos da Empresa
        widgets = {
            'cnpj': forms.TextInput(attrs={'class': 'cnpj-mask'}),
        }
        
    class ResendActivationEmailForm(forms.Form):
        email = forms.EmailField(label="E-mail", widget=forms.TextInput(attrs={'placeholder': 'Digite o e-mail cadastrado'}))