# gerenciamento_artigos/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from tinymce.models import HTMLField

class Artigo(models.Model):
    # ... (as CHOICES continuam as mesmas)
    CATEGORIA_CHOICES = (
        ('legislacao-fiscal-e-aduaneira', 'Legislações Fiscal e Aduaneira'),
        ('acordos-comerciais', 'Acordos Comerciais'),
        ('regulamentos-internacionais', 'Regulamentos Internacionais'),
        ('invista-em-roraima', 'Invista em Roraima'),
        ('prospeccao-de-mercados', 'Prospecção de Mercados'),
    )
    TIPO_CONTEUDO_CHOICES = (('TEXTO', 'Artigo de Texto'), ('PDF', 'Documento PDF'),)
    STATUS_CHOICES = (('RASCUNHO', 'Rascunho'), ('PUBLICADO', 'Publicado'),)
    
    categoria = models.CharField(max_length=100, choices=CATEGORIA_CHOICES, verbose_name="Categoria/Subárea")
    titulo = models.CharField(max_length=200, unique=True, verbose_name="Título")
    subtitulo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Subtítulo (Opcional)")
    slug = models.SlugField(max_length=255, unique=True, blank=True, help_text="Este campo é preenchido automaticamente a partir do título.")
    imagem_card = models.ImageField(upload_to='artigos/cards/', verbose_name="Imagem do Card", help_text="Imagem que aparecerá na listagem principal. Tamanho ideal: 800x600 pixels.")
    
    # --- NOVO CAMPO ADICIONADO ABAIXO ---
    resumo_destaque = HTMLField(blank=True, null=True, verbose_name="Resumo / Pontos-Chave (Opcional)", help_text="Conteúdo a ser exibido em uma caixa de destaque no topo do artigo.")

    tipo_conteudo = models.CharField(max_length=10, choices=TIPO_CONTEUDO_CHOICES, default='TEXTO', verbose_name="Tipo de Conteúdo")
    corpo_conteudo = HTMLField(blank=True, verbose_name="Corpo do Artigo (se for texto)", help_text="Utilize este campo se o tipo de conteúdo for 'Artigo de Texto'.")
    arquivo_pdf = models.FileField(upload_to='artigos/pdfs/', blank=True, null=True, verbose_name="Arquivo PDF", help_text="Faça o upload do arquivo se o tipo de conteúdo for 'Documento PDF'.")
    
    autor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='artigos_autor', verbose_name="Autor", editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='RASCUNHO', verbose_name="Status")
    
    meta_descricao = models.TextField(max_length=160, blank=True, null=True, verbose_name="Descrição para SEO", help_text="Resumo do artigo para o Google (máximo de 160 caracteres).")
    palavras_chave = models.CharField(max_length=255, blank=True, null=True, verbose_name="Palavras-chave", help_text="Palavras-chave separadas por vírgula (ex: acordo comercial, legislação, roraima).")

    data_publicacao = models.DateTimeField(default=timezone.now, verbose_name="Data de Publicação")
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    # ... (o restante dos métodos e da classe Meta continuam iguais)
    def clean(self):
        super().clean()
        if self.tipo_conteudo == 'TEXTO' and not self.corpo_conteudo:
            raise ValidationError({'corpo_conteudo': 'Para "Artigo de Texto", o corpo do artigo não pode ficar em branco.'})
        if self.tipo_conteudo == 'PDF' and not self.arquivo_pdf:
            raise ValidationError({'arquivo_pdf': 'Para "Documento PDF", você precisa enviar um arquivo.'})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Artigo"
        verbose_name_plural = "Artigos"
        ordering = ['-data_publicacao']