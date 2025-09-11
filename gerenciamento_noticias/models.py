from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from tinymce.models import HTMLField
from django.utils import timezone
from taggit.managers import TaggableManager

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Categoria")
    slug = models.SlugField(max_length=120, unique=True, blank=True, help_text="Este campo é preenchido automaticamente.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Categoria de Notícia"
        verbose_name_plural = "1. Categorias de Notícias"
        ordering = ['nome']

class Noticia(models.Model):
    STATUS_CHOICES = (
        ('RASCUNHO', 'Rascunho'),
        ('PUBLICADO', 'Publicado'),
    )

    titulo = models.CharField(max_length=200, unique=True, verbose_name="Título da Notícia")
    slug = models.SlugField(max_length=255, unique=True, blank=True, help_text="Preenchido automaticamente a partir do título.")
    subtitulo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Subtítulo (Opcional)")
    corpo = HTMLField(verbose_name="Corpo da Notícia")
    imagem_card = models.ImageField(upload_to='noticias/cards/', verbose_name="Imagem de Capa/Card", help_text="Imagem principal da matéria.")
    autor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='noticias_autor', verbose_name="Autor")
    categorias = models.ManyToManyField(Categoria, related_name='noticias', verbose_name="Categorias")
    tags = TaggableManager(verbose_name="Tags", help_text="Uma lista de tags separadas por vírgula.", blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='RASCUNHO', verbose_name="Status")
    data_publicacao = models.DateTimeField(default=timezone.now, verbose_name="Data de Publicação")
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "2. Notícias"
        ordering = ['-data_publicacao']

class NoticiaDestaque(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, verbose_name="Notícia em Destaque", help_text="Selecione a notícia que aparecerá no carrossel.")
    ordem = models.PositiveIntegerField(default=0, verbose_name="Ordem de Exibição", help_text="Um número menor aparece primeiro (0, 1, 2...).")
    
    def __str__(self):
        return f"Destaque {self.ordem}: {self.noticia.titulo}"

    class Meta:
        verbose_name = "Notícia em Destaque"
        verbose_name_plural = "3. Notícias em Destaque"
        ordering = ['ordem']
        
class BannerNoticias(models.Model):
    TIPO_CHOICES = [
        ('IMAGEM_TEXTO', 'Imagem de Fundo com Texto Sobreposto'),
        ('TEXTO_ESTATICO', 'Apenas Texto Estático'),
        ('ANIMACAO_JS', 'Animação com Código JavaScript'),
    ]
    tipo_conteudo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='IMAGEM_TEXTO',
        verbose_name="Tipo de Conteúdo do Banner"
    )
    titulo = models.CharField(max_length=150, verbose_name="Título", blank=True)
    subtitulo = models.TextField(blank=True, verbose_name="Subtítulo/Texto (Opcional)")
    imagem_fundo = models.ImageField(
        upload_to='noticias/banners/',
        verbose_name="Imagem de Fundo",
        blank=True, null=True,
        help_text="Usado apenas para o tipo 'Imagem de Fundo'."
    )
    codigo_js = models.TextField(
        blank=True,
        verbose_name="Código JavaScript",
        help_text="Cole aqui o script completo da animação. Ele será renderizado na página."
    )
    ativo = models.BooleanField(default=False, verbose_name="Está ativo?", help_text="Apenas um banner pode estar ativo por vez.")

    def save(self, *args, **kwargs):
        if self.ativo:
            BannerNoticias.objects.filter(ativo=True).exclude(pk=self.pk).update(ativo=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo or f"Banner do tipo {self.get_tipo_conteudo_display()}"

    class Meta:
        verbose_name = "Banner da Página de Notícias"
        verbose_name_plural = "0. Banners da Página de Notícias"