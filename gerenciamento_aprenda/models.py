# Arquivo: gerenciamento_aprenda/models.py

from django.db import models

class ConteudoApresentacaoAprenda(models.Model):
    TIPO_CHOICES = [
        ('IMAGEM', 'Imagem Estática'),
        ('VIDEO', 'Vídeo (YouTube)'),
    ]

    descricao = models.CharField(
        max_length=200,
        verbose_name="Descrição Interna",
        help_text="Ex: 'Vídeo institucional de lançamento' ou 'Imagem da campanha de Setembro'."
    )
    tipo_conteudo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        default='IMAGEM',
        verbose_name="Tipo de Conteúdo"
    )
    imagem = models.ImageField(
        upload_to='aprenda/apresentacao/',
        blank=True,
        null=True,
        verbose_name="Arquivo de Imagem",
        help_text="Carregue uma imagem se o tipo for 'Imagem Estática'."
    )
    video_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="URL do Vídeo do YouTube",
        help_text="Cole a URL normal do vídeo do YouTube. Ex: https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )
    em_exibicao = models.BooleanField(
        default=False,
        verbose_name="Em exibição na página?",
        help_text="Marque esta opção para que este conteúdo apareça na página. Apenas um pode estar em exibição."
    )

    def get_embed_url(self):
        """
        Converte uma URL normal do YouTube para a URL de incorporação (embed).
        """
        if self.video_url and 'watch?v=' in self.video_url:
            video_id = self.video_url.split('watch?v=')[1].split('&')[0]
            return f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&loop=1&playlist={video_id}&controls=0"
        return None

    def save(self, *args, **kwargs):
        # Garante que apenas um item possa estar em exibição por vez.
        if self.em_exibicao:
            ConteudoApresentacaoAprenda.objects.filter(em_exibicao=True).update(em_exibicao=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Conteúdo de Apresentação (Aprenda Comex)"
        verbose_name_plural = "1. Conteúdos de Apresentação (Aprenda Comex)"