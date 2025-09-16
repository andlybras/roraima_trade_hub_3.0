from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField

class ConteudoApresentacaoDestino(models.Model):
    TIPO_CHOICES = [
        ('IMAGEM', 'Imagem Estática'),
        ('VIDEO', 'Vídeo (YouTube)'),
        ('ANIMACAO_JS', 'Animação com Código JavaScript')
    ]
    descricao = models.CharField(max_length=200, verbose_name="Descrição Interna")
    tipo_conteudo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES, 
        default='IMAGEM', 
        verbose_name="Tipo de Conteúdo"
    )
    imagem = models.ImageField(
        upload_to='destino/apresentacao/', 
        blank=True, null=True, 
        verbose_name="Arquivo de Imagem",
        help_text="Usado apenas para o tipo 'Imagem Estática'."
    )
    video_url = models.URLField(
        blank=True, null=True, 
        verbose_name="URL do Vídeo do YouTube",
        help_text="Usado apenas para o tipo 'Vídeo (YouTube)'."
    )
    codigo_js = models.TextField(
        blank=True,
        verbose_name="Código JavaScript da Animação",
        help_text="Usado apenas para o tipo 'Animação'. Cole o código JS completo aqui."
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
            ConteudoApresentacaoDestino.objects.filter(em_exibicao=True).exclude(pk=self.pk).update(em_exibicao=False)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.descricao
    class Meta:
        verbose_name = "Artifício de Apresentação do Módulo"
        verbose_name_plural = "Artifícios de Apresentação do Módulo"

class Categoria(models.Model):
    GRUPOS = [
        ('NATUREZA', 'Belezas da Natureza'),
        ('CULTURA', 'Cultura e Tradições'),
    ]
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Categoria")
    slug = models.SlugField(max_length=120, unique=True, blank=True, help_text="Este campo é preenchido automaticamente.")
    grupo = models.CharField(max_length=10, choices=GRUPOS, verbose_name="Grupo", help_text="Associe esta categoria a uma das grandes áreas do módulo.")
    icone = models.FileField(upload_to='destino/icones/', blank=True, null=True, verbose_name="Ícone (SVG)", help_text="Ícone que aparecerá no mapa. Use formato SVG, se possível.")
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.nome} ({self.get_grupo_display()})"
    class Meta:
        verbose_name = "Categoria (para Filtros)"
        verbose_name_plural = "Categorias (para Filtros)"
        ordering = ['grupo', 'nome']

class PontoDeInteresse(models.Model):
    titulo = models.CharField(max_length=200, unique=True, verbose_name="Título do Ponto de Interesse")
    slug = models.SlugField(max_length=255, unique=True, blank=True, help_text="Preenchido automaticamente a partir do título.")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, verbose_name="Categoria")
    descricao_curta = models.TextField(max_length=250, verbose_name="Descrição Curta", help_text="Texto que aparece na janela do mapa (máx. 250 caracteres).")
    descricao_completa = HTMLField(verbose_name="Descrição Completa", help_text="Toda a história e detalhes do local.")
    imagem_principal = models.ImageField(upload_to='destino/pontos_interesse/', verbose_name="Imagem Principal", help_text="A imagem de maior destaque na página do local.")
    latitude = models.DecimalField(max_digits=10, decimal_places=7, verbose_name="Latitude", help_text="Coordenada de latitude. Ex: 2.8235241")
    longitude = models.DecimalField(max_digits=10, decimal_places=7, verbose_name="Longitude", help_text="Coordenada de longitude. Ex: -60.6758335")
    informacoes_praticas = HTMLField(verbose_name="Informações Práticas", help_text="Use listas e negrito para formatar dicas como 'O que levar', 'Melhor época', 'Como chegar', etc.")
    publicado = models.BooleanField(default=False, verbose_name="Publicado?")
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.titulo
    class Meta:
        verbose_name = "Ponto de Interesse"
        verbose_name_plural = "Pontos de Interesse"
        ordering = ['titulo']

class ImagemGaleria(models.Model):
    ponto_de_interesse = models.ForeignKey(PontoDeInteresse, related_name='galeria_imagens', on_delete=models.CASCADE, verbose_name="Ponto de Interesse")
    imagem = models.ImageField(upload_to='destino/galerias/', verbose_name="Imagem")
    legenda = models.CharField(max_length=150, blank=True, verbose_name="Legenda (Opcional)")
    def __str__(self):
        return f"Imagem para {self.ponto_de_interesse.titulo}"
    class Meta:
        verbose_name = "Imagem da Galeria"
        verbose_name_plural = "Imagens da Galeria"

class Roteiro(models.Model):
    titulo = models.CharField(max_length=200, unique=True, verbose_name="Título do Roteiro")
    slug = models.SlugField(max_length=255, unique=True, blank=True, help_text="Preenchido automaticamente a partir do título.")
    descricao = HTMLField(verbose_name="Descrição do Roteiro")
    pontos_de_interesse = models.ManyToManyField(PontoDeInteresse, through='OrdemPontoRoteiro', verbose_name="Pontos de Interesse")
    imagem_capa = models.ImageField(upload_to='destino/roteiros/', verbose_name="Imagem de Capa do Roteiro")
    publicado = models.BooleanField(default=False, verbose_name="Publicado?")
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.titulo
    class Meta:
        verbose_name = "Roteiro Temático"
        verbose_name_plural = "Roteiros Temáticos"

class OrdemPontoRoteiro(models.Model):
    roteiro = models.ForeignKey(Roteiro, on_delete=models.CASCADE)
    ponto_de_interesse = models.ForeignKey(PontoDeInteresse, on_delete=models.CASCADE)
    ordem = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['ordem']
        verbose_name = "Ordem do Ponto no Roteiro"
        verbose_name_plural = "Ordens dos Pontos nos Roteiros"