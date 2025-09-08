# Arquivo: gerenciamento_acordos/models.py

from django.db import models

class ConteudoApresentacaoAcordos(models.Model):
    TIPO_CHOICES = [('IMAGEM', 'Imagem Estática'), ('VIDEO', 'Vídeo (YouTube)')]
    descricao = models.CharField(max_length=200, verbose_name="Descrição Interna", help_text="Ex: 'Imagem de aperto de mãos'.")
    tipo_conteudo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='IMAGEM', verbose_name="Tipo de Conteúdo")
    imagem = models.ImageField(upload_to='acordos/apresentacao/', blank=True, null=True, verbose_name="Arquivo de Imagem")
    video_url = models.URLField(blank=True, null=True, verbose_name="URL do Vídeo do YouTube")
    em_exibicao = models.BooleanField(default=False, verbose_name="Em exibição na página?", help_text="Apenas um conteúdo pode estar em exibição.")

    def get_embed_url(self):
        if self.video_url and 'watch?v=' in self.video_url:
            video_id = self.video_url.split('watch?v=')[1].split('&')[0]
            return f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&loop=1&playlist={video_id}&controls=0"
        return None

    def save(self, *args, **kwargs):
        if self.em_exibicao:
            ConteudoApresentacaoAcordos.objects.filter(em_exibicao=True).update(em_exibicao=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Conteúdo de Apresentação (Acordos)"
        verbose_name_plural = "3. Conteúdos de Apresentação (Acordos)"