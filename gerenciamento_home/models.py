from django.db import models

class HeaderLogo(models.Model):
    descricao = models.CharField(max_length=100, help_text="Descrição interna do logotipo (ex: Logo Governo RR).")
    imagem = models.ImageField(upload_to='logos/header/', help_text="Faça upload da imagem do logo.")
    link_url = models.URLField(max_length=200, blank=True, null=True, help_text="Link opcional para o logo.")

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Logotipo do Cabeçalho"
        verbose_name_plural = "1. Manutenção Logotipos (Cabeçalho)"

class ImagemApresentacao(models.Model):
    TIPO_CHOICES = [
        ('FUNDO', 'Imagem de Fundo do Site'),
        ('HERO', 'Imagem do Carrossel (Hero)'),
    ]    
    tipo = models.CharField(max_length=5, choices=TIPO_CHOICES, default='HERO')
    descricao = models.CharField(max_length=100, help_text="Descrição interna da imagem (ex: Paisagem RR).")
    imagem = models.ImageField(upload_to='apresentacao/', help_text="Imagem principal da home page ou fundo do site.")
    link_url = models.URLField(max_length=200, blank=True, null=True, help_text="Link opcional para a imagem.")
    ordem = models.PositiveIntegerField(default=0, help_text="Use 0, 1, 2... para definir a ordem de aparição no carrossel.")

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.descricao}"

    class Meta:
        verbose_name = "Imagem de Apresentação"
        verbose_name_plural = "2. Manutenção Imagens (Fundo e Hero)"
        ordering = ['ordem']

class PartnerLogo(models.Model):
    nome_parceiro = models.CharField(max_length=100, help_text="Nome do parceiro.")
    imagem = models.ImageField(upload_to='logos/parceiros/', help_text="Logo do parceiro para o carrossel do rodapé.")
    link_url = models.URLField(max_length=200, blank=True, null=True, help_text="Link opcional para o site do parceiro.")
    ordem = models.PositiveIntegerField(default=0, help_text="Use 0, 1, 2... para definir a ordem no carrossel.")

    def __str__(self):
        return self.nome_parceiro

    class Meta:
        verbose_name = "Logotipo de Parceiro"
        verbose_name_plural = "3. Manutenção Logotipos (Parceiros)"
        ordering = ['ordem']