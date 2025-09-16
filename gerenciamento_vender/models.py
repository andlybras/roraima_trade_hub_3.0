# gerenciamento_vender/models.py

from django.db import models
from tinymce.models import HTMLField
import uuid

# === CÓDIGO EXISTENTE (MANTER) ===
class ConteudoApresentacaoVender(models.Model):
    TIPO_CHOICES = [
        ('IMAGEM', 'Imagem Estática'),
        ('VIDEO', 'Vídeo (YouTube)'),
    ]

    descricao = models.CharField(
        max_length=200,
        verbose_name="Descrição Interna",
        help_text="Ex: 'Vídeo sobre como vender' ou 'Imagem da vitrine de produtos'."
    )
    tipo_conteudo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        default='IMAGEM',
        verbose_name="Tipo de Conteúdo"
    )
    imagem = models.ImageField(
        upload_to='vender/apresentacao/',
        blank=True,
        null=True,
        verbose_name="Arquivo de Imagem",
        help_text="Carregue uma imagem se o tipo for 'Imagem Estática'."
    )
    video_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="URL do Vídeo do YouTube",
        help_text="Cole a URL normal do vídeo do YouTube."
    )
    em_exibicao = models.BooleanField(
        default=False,
        verbose_name="Em exibição na página?",
        help_text="Apenas um conteúdo pode estar em exibição."
    )

    def get_embed_url(self):
        if self.video_url and 'watch?v=' in self.video_url:
            video_id = self.video_url.split('watch?v=')[1].split('&')[0]
            return f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&loop=1&playlist={video_id}&controls=0"
        return None

    def save(self, *args, **kwargs):
        if self.em_exibicao:
            ConteudoApresentacaoVender.objects.filter(em_exibicao=True).update(em_exibicao=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Artifício de Apresentação do Módulo"
        verbose_name_plural = "Artifícios de Apresentação do Módulo"


# === NOVO CÓDIGO (ADICIONAR ABAIXO) ===

# Modelo para as Perguntas Frequentes públicas (gerenciadas pelo admin)
class PerguntaFrequente(models.Model):
    pergunta = models.CharField(max_length=255, verbose_name="Pergunta")
    resposta = HTMLField(verbose_name="Resposta")
    publicada = models.BooleanField(default=False, verbose_name="Está publicada?")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    def __str__(self):
        return self.pergunta

    class Meta:
        verbose_name = "Pergunta Frequente"
        verbose_name_plural = "Perguntas Frequentes"
        ordering = ['pergunta']


# Modelo para as perguntas enviadas pelos usuários
class PerguntaUsuario(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente de Resposta'),
        ('RESPONDIDA', 'Respondida'),
    ]

    # Campo para a avaliação da resposta pelo usuário
    AVALIACAO_CHOICES = [
        (True, 'Útil'),
        (False, 'Não foi útil'),
    ]

    # Campos da Pergunta
    pergunta = models.TextField(verbose_name="Pergunta do Usuário")
    email_usuario = models.EmailField(verbose_name="E-mail do Usuário")
    data_envio = models.DateTimeField(auto_now_add=True, verbose_name="Data de Envio")
    
    # Campos da Resposta (gerenciados pelo admin)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE', verbose_name="Status")
    resposta = HTMLField(verbose_name="Resposta do Administrador", blank=True, null=True)
    data_resposta = models.DateTimeField(verbose_name="Data da Resposta", blank=True, null=True)

    # Campos de controle
    identificador_unico = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="Identificador Único")
    resposta_foi_util = models.BooleanField(choices=AVALIACAO_CHOICES, null=True, blank=True, verbose_name="Avaliação do Usuário")


    def __str__(self):
        return f"Pergunta de {self.email_usuario} em {self.data_envio.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Pergunta de Usuário"
        verbose_name_plural = "Perguntas de Usuários"
        ordering = ['-data_envio']
        
class DadosEmpresariais(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente de preenchimento'),
        ('EM_ANALISE', 'Em Análise'),
        ('APROVADO', 'Aprovado'),
        ('REAVALIACAO', 'Aprovado (em Reavaliação)'),
    ]

    # Relacionamento com o usuário (será ajustado quando tivermos autenticação)
    # Por enquanto, este campo não é obrigatório para podermos testar.
    usuario = models.OneToOneField(
        'auth.User', 
        on_delete=models.CASCADE, 
        verbose_name="Usuário",
        null=True, blank=True 
    )

    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='PENDENTE', 
        verbose_name="Status do Cadastro"
    )

    # Etapa 1: Dados da Empresa
    nome_fantasia = models.CharField(max_length=255, verbose_name="Nome Fantasia")
    razao_social = models.CharField(max_length=255, verbose_name="Razão Social")
    cnpj = models.CharField(max_length=18, verbose_name="CNPJ")
    inscricao_estadual = models.CharField(max_length=20, verbose_name="Inscrição Estadual")
    atividade_principal = models.TextField(verbose_name="Atividade Comercial Principal")
    atividades_secundarias = models.TextField(verbose_name="Atividades Comerciais Secundárias", blank=True)
    documento_comprobatorio_empresa = models.FileField(
        upload_to='documentos/empresa/', 
        verbose_name="Documento Comprobatório da Empresa"
    )

    # Etapa 2: Dados do Responsável
    nome_responsavel = models.CharField(max_length=255, verbose_name="Nome Completo do Responsável")
    cpf_responsavel = models.CharField(max_length=14, verbose_name="CPF do Responsável")
    cargo_responsavel = models.CharField(max_length=100, verbose_name="Cargo do Responsável")
    email_responsavel = models.EmailField(verbose_name="E-mail para Contato Direto")
    telefone_responsavel = models.CharField(max_length=20, verbose_name="Telefone/WhatsApp para Contato")
    documento_vinculo_responsavel = models.FileField(
        upload_to='documentos/responsavel/', 
        verbose_name="Documento Comprobatório do Vínculo"
    )

    # Etapa 3: Dados Complementares
    endereco = models.TextField(verbose_name="Endereço Completo")
    telefone_institucional = models.CharField(max_length=20, blank=True, verbose_name="Telefone Institucional")
    email_institucional = models.EmailField(blank=True, verbose_name="E-mail Institucional")
    website = models.URLField(blank=True, verbose_name="Website")
    apresentacao_empresa = models.TextField(blank=True, verbose_name="Apresentação da Empresa")

    # Datas de controle
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome_fantasia or self.razao_social

    class Meta:
        verbose_name = "Dados Empresariais"
        verbose_name_plural = "Dados Empresariais"