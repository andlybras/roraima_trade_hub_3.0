# Arquivo: gerenciamento_home/views.py

from django.shortcuts import render
from .models import HeaderLogo, ImagemApresentacao, PartnerLogo

def home(request):
    """
    Esta view busca todos os objetos necessários para a home page
    e os envia para o template.
    """
    header_logos = HeaderLogo.objects.all()
    hero_images = ImagemApresentacao.objects.filter(tipo='HERO').order_by('ordem')
    partner_logos = PartnerLogo.objects.order_by('ordem')
    imagem_fundo = ImagemApresentacao.objects.filter(tipo='FUNDO').first()

    # O 'context' é um dicionário que leva as informações do Python para o HTML
    context = {
        'header_logos': header_logos,
        'hero_images': hero_images,
        'partner_logos': partner_logos,
        'imagem_fundo': imagem_fundo,
    }

    return render(request, 'gerenciamento_home/html/home.html', context)