# gerenciamento_home/context_processors.py

from gerenciamento_home.models import HeaderLogo, ImagemApresentacao, PartnerLogo
from gerenciamento_vender.models import DadosEmpresariais

def global_context(request):
    contexto = {
        'header_logos': HeaderLogo.objects.all(),
        'partner_logos': PartnerLogo.objects.order_by('ordem'),
        # LINHA CORRIGIDA: Adicionando de volta a busca pela imagem de fundo
        'imagem_fundo': ImagemApresentacao.objects.filter(tipo='FUNDO').first(),
    }

    # Lógica para buscar os dados da empresa do usuário logado
    if request.user.is_authenticated:
        try:
            dados_empresa = DadosEmpresariais.objects.get(usuario=request.user)
            contexto['dados_empresa'] = dados_empresa
        except DadosEmpresariais.DoesNotExist:
            pass

    return contexto