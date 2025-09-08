from django.shortcuts import render
from .models import HeaderLogo, ImagemApresentacao, PartnerLogo

def home(request):
    header_logos = HeaderLogo.objects.all()
    hero_images = ImagemApresentacao.objects.filter(tipo='HERO').order_by('ordem')
    partner_logos = PartnerLogo.objects.order_by('ordem')
    imagem_fundo = ImagemApresentacao.objects.filter(tipo='FUNDO').first()
    context = {
        'header_logos': header_logos,
        'hero_images': hero_images,
        'partner_logos': partner_logos,
        'imagem_fundo': imagem_fundo,
    }
    return render(request, 'gerenciamento_home/html/home.html', context)