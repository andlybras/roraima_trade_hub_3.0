from .models import HeaderLogo, ImagemApresentacao, PartnerLogo

def global_context(request):
    return {
        'header_logos': HeaderLogo.objects.all(),
        'imagem_fundo': ImagemApresentacao.objects.filter(tipo='FUNDO').first(),
        'partner_logos': PartnerLogo.objects.order_by('ordem'),
    }