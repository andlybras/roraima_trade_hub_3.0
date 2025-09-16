from django import forms
from .models import DadosEmpresariais
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField

class DadosEmpresaForm(forms.ModelForm):
    class Meta:
        model = DadosEmpresariais
        fields = [
            'nome_fantasia', 'razao_social', 'cnpj', 'inscricao_estadual',
            'atividade_principal', 'atividades_secundarias', 'documento_comprobatorio_empresa'
        ]
        widgets = {
            'nome_fantasia': forms.TextInput(attrs={'class': 'form-input'}),
            'razao_social': forms.TextInput(attrs={'class': 'form-input'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-input'}),
            'inscricao_estadual': forms.TextInput(attrs={'class': 'form-input'}),
            'atividade_principal': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'atividades_secundarias': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'documento_comprobatorio_empresa': forms.FileInput(attrs={'class': 'form-input'}),
        }

class DadosResponsavelForm(forms.ModelForm):
    class Meta:
        model = DadosEmpresariais
        fields = [
            'nome_responsavel', 'cpf_responsavel', 'cargo_responsavel',
            'email_responsavel', 'telefone_responsavel', 'documento_vinculo_responsavel'
        ]
        widgets = {
            'nome_responsavel': forms.TextInput(attrs={'class': 'form-input'}),
            'cpf_responsavel': forms.TextInput(attrs={'class': 'form-input'}),
            'cargo_responsavel': forms.TextInput(attrs={'class': 'form-input'}),
            'email_responsavel': forms.EmailInput(attrs={'class': 'form-input'}),
            'telefone_responsavel': forms.TextInput(attrs={'class': 'form-input'}),
            'documento_vinculo_responsavel': forms.FileInput(attrs={'class': 'form-input'}),
        }

class DadosComplementaresForm(forms.ModelForm):
    class Meta:
        model = DadosEmpresariais
        fields = [
            'endereco', 'telefone_institucional', 'email_institucional',
            'website', 'apresentacao_empresa'
        ]
        widgets = {
            'endereco': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'telefone_institucional': forms.TextInput(attrs={'class': 'form-input'}),
            'email_institucional': forms.EmailInput(attrs={'class': 'form-input'}),
            'website': forms.URLInput(attrs={'class': 'form-input'}),
            'apresentacao_empresa': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5}),
        }
        
class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-input'})
    )
    email2 = forms.EmailField(
        label='Confirme o E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-input'})
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    password2 = forms.CharField(
        label='Confirme a Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    terms = forms.BooleanField(
        label='Eu li e aceito os Termos de Uso e a Política de Privacidade',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ('email',)

    def clean_email2(self):
        cd = self.cleaned_data
        if cd['email'] != cd['email2']:
            raise forms.ValidationError('Os e-mails não coincidem.')
        return cd['email2']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('As senhas não coincidem.')
        return cd['password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está cadastrado em nosso sistema.')
        return email