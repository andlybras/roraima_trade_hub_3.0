# Arquivo: gerenciamento_registros/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from tinymce.models import HTMLField

class CustomUser(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('PERMISSIONARIO', 'Permissionário (Equipe Interna)'),
        ('EMPRESA', 'Empresa'),
        ('EMPREENDEDOR', 'Empreendedor'),
        ('APRENDIZ', 'Aprendiz (Aprenda Comex)'),
    ]
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        verbose_name="Tipo de Usuário",
        # Removemos o default para garantir que seja sempre definido
    )
    is_email_verified = models.BooleanField(
        default=False,
        verbose_name="E-mail verificado"
    )

class PermissionarioProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='permissionario_profile')
    orgao_lotacao = models.CharField(max_length=255, verbose_name="Órgão/Lotação")

    def __str__(self):
        return self.user.get_full_name() or self.user.username
    
    class Meta:
        verbose_name = "Perfil de Permissionário"
        verbose_name_plural = "Perfis de Permissionários"

class AprendizProfile(models.Model):
    NIVEL_CONHECIMENTO_CHOICES = [
        ('INICIANTE', 'Iniciante (Nunca estudei/trabalhei com Comex)'),
        ('INTERMEDIARIO', 'Intermediário (Já tive algum contato ou estudei o básico)'),
        ('AVANCADO', 'Avançado (Trabalho ou tenho conhecimento sólido na área)'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='aprendiz_profile')
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    residencia = models.CharField(max_length=100, verbose_name="Estado/País de Residência")
    nivel_conhecimento_comex = models.CharField(
        max_length=20,
        choices=NIVEL_CONHECIMENTO_CHOICES,
        verbose_name="Nível de conhecimento em Comércio Exterior"
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    class Meta:
        verbose_name = "Perfil de Aprendiz"
        verbose_name_plural = "Perfis de Aprendizes"

class ModeloEmail(models.Model):
    identificador = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="Identificador Único",
        help_text="Um nome curto, sem espaços ou caracteres especiais (ex: 'ativacao-conta', 'reset-senha'). Usado internamente pelo sistema."
    )
    assunto = models.CharField(max_length=200, verbose_name="Assunto do E-mail")
    corpo = HTMLField(
        verbose_name="Corpo do E-mail",
        help_text="O conteúdo do e-mail. Você pode usar variáveis como {{ user.username }}, {{ link_ativacao }}, etc., que serão substituídas dinamicamente."
    )

    def __str__(self):
        return self.assunto

    class Meta:
        verbose_name = "Modelo de E-mail"
        verbose_name_plural = "4. Central de Comunicação (Modelos de E-mail)"

# --- MODELOS DE PERFIL FALTANTES ---
class EmpreendedorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='empreendedor_profile')
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo", blank=True)
    cpf = models.CharField(max_length=14, verbose_name="CPF", blank=True)
    # ... outros campos futuros para empreendedor

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Perfil de Empreendedor"
        verbose_name_plural = "Perfis de Empreendedores"


class EmpresaProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='empresa_profile')
    nome_fantasia = models.CharField(max_length=255, verbose_name="Nome Fantasia", blank=True)
    razao_social = models.CharField(max_length=255, verbose_name="Razão Social", blank=True)
    cnpj = models.CharField(max_length=18, verbose_name="CNPJ", blank=True)
    # ... outros campos futuros para empresa

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Perfil de Empresa"
        verbose_name_plural = "Perfis de Empresas"