from django.db import models
import uuid
from tinymce.models import HTMLField

class ConteudoInteligencia(models.Model):
    CATEGORIAS = [
        ('DADOS_ESTRUTURAIS', 'Dados Estruturais'),
        ('ANALISES_E_ARTIGOS', 'Análises'),
    ]

    categoria = models.CharField(max_length=50, choices=CATEGORIAS, verbose_name="Categoria do Conteúdo")
    titulo_card = models.CharField(max_length=100, verbose_name="Título no Card", help_text="Texto que aparece na listagem de cards da seção.")
    imagem_card = models.ImageField(upload_to='inteligencia_mercado/cards/', verbose_name="Imagem de Capa do Card", help_text="Imagem que aparece na listagem de cards.")
    titulo_pagina = models.CharField(max_length=200, verbose_name="Título Principal da Página", help_text="Título exibido no topo da página ao abrir o conteúdo.")
    subtitulo_pagina = models.CharField(max_length=300, blank=True, null=True, verbose_name="Subtítulo da Página", help_text="Texto curto opcional que aparece abaixo do título principal.")
    corpo_conteudo = HTMLField(
        verbose_name="Conteúdo Principal",
        help_text="O texto principal do artigo. Use a tag [grafico:sua-chave-aqui] para inserir um gráfico no texto."
    )
    publicado = models.BooleanField(
        default=False,
        verbose_name="Visível para o público?",
        help_text="Marque esta opção para que o conteúdo apareça no site para os usuários."
    )

    def __str__(self):
        return self.titulo_card

    class Meta:
        verbose_name = "Publicação"
        verbose_name_plural = "Publicações"
        ordering = ['categoria', 'titulo_card']

class Grafico(models.Model):
    TIPO_CHOICES = [
        ('OPTION_SIMPLE', 'Objeto Option Simples'),
        ('SCRIPT_COMPLETO', 'Script de Animação Completo'),
    ]

    tipo_grafico = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='OPTION_SIMPLE',
        verbose_name="Tipo de Gráfico",
        help_text="Escolha 'Objeto Option Simples' se você está colando apenas o JSON de configuração. Escolha 'Script de Animação Completo' para colar um script JavaScript auto-executável."
    )
    titulo = models.CharField(max_length=200, unique=True, verbose_name="Título Interno do Gráfico", help_text="Um nome único para identificar o gráfico no painel.")
    chave = models.CharField(max_length=10, unique=True, blank=True, editable=False, verbose_name="Chave Única")
    codigo_js_echarts = models.TextField(verbose_name="Código JavaScript", help_text="Cole aqui o objeto 'option' ou o script completo, de acordo com o tipo selecionado acima.")
    is_grafico_principal = models.BooleanField(
        default=False,
        verbose_name="É o gráfico principal da página de Inteligência?",
        help_text="Marque esta opção para que este gráfico apareça na página inicial do módulo de Inteligência de Mercado. Apenas um pode ser marcado."
    )

    def save(self, *args, **kwargs):
        if not self.chave:
            self.chave = f"g-{uuid.uuid4().hex[:6]}"
        if self.is_grafico_principal:
            Grafico.objects.filter(is_grafico_principal=True).exclude(pk=self.pk).update(is_grafico_principal=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Gráfico"
        verbose_name_plural = "Gráficos"

class TermoGlossario(models.Model):
    termo = models.CharField(max_length=100, unique=True, verbose_name="Termo")
    explicacao = HTMLField(
        verbose_name="Explicação do Termo",
        help_text="Use as ferramentas de formatação para criar uma explicação clara e didática."
    )

    def __str__(self):
        return self.termo

    class Meta:
        verbose_name = "Termo"
        verbose_name_plural = "Termos"
        ordering = ['termo']