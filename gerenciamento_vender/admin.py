# gerenciamento_vender/admin.py

from django.contrib import admin
from .models import ConteudoApresentacaoVender, PerguntaFrequente, PerguntaUsuario, DadosEmpresariais
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

# --- CONFIGURAÇÕES EXISTENTES (MANTER) ---
@admin.register(ConteudoApresentacaoVender)
class ConteudoApresentacaoVenderAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'tipo_conteudo', 'em_exibicao')
    list_filter = ('tipo_conteudo', 'em_exibicao')

@admin.register(PerguntaFrequente)
class PerguntaFrequenteAdmin(admin.ModelAdmin):
    list_display = ('pergunta', 'publicada', 'data_criacao')
    list_filter = ('publicada',)
    search_fields = ('pergunta', 'resposta')
    list_per_page = 20

@admin.register(PerguntaUsuario)
class PerguntaUsuarioAdmin(admin.ModelAdmin):
    # (código existente, sem alterações)
    list_display = ('pergunta_resumida', 'email_usuario', 'status', 'data_envio', 'resposta_foi_util')
    list_filter = ('status', 'resposta_foi_util', 'data_envio')
    search_fields = ('pergunta', 'email_usuario', 'resposta')
    list_per_page = 20
    fieldsets = (
        ('Informações do Usuário (Não editável)', {'fields': ('email_usuario', 'pergunta', 'data_envio', 'identificador_unico')}),
        ('Resposta do Administrador', {'fields': ('status', 'resposta')}),
        ('Feedback do Usuário (Preenchido por ele)', {'classes': ('collapse',),'fields': ('resposta_foi_util', 'data_resposta'),}),
    )
    readonly_fields = ('email_usuario', 'pergunta', 'data_envio', 'data_resposta', 'identificador_unico', 'resposta_foi_util')
    def pergunta_resumida(self, obj):
        return obj.pergunta[:70] + '...' if len(obj.pergunta) > 70 else obj.pergunta
    pergunta_resumida.short_description = 'Pergunta do Usuário'
    def save_model(self, request, obj, form, change):
        enviar_email = False
        if 'resposta' in form.changed_data and obj.resposta and obj.status != 'RESPONDIDA':
            obj.status = 'RESPONDIDA'
            obj.data_resposta = timezone.now()
            enviar_email = True
        super().save_model(request, obj, form, change)
        if enviar_email:
            link_resposta = request.build_absolute_uri(reverse('vender:ver_resposta', args=[obj.identificador_unico]))
            contexto_email = {'pergunta': obj, 'link_resposta': link_resposta}
            corpo_email = render_to_string('gerenciamento_vender/html/emails/resposta_disponivel.txt', contexto_email)
            send_mail('Sua pergunta foi respondida! - Roraima Trade Hub', corpo_email, 'nao-responda@roraimatradehub.com', [obj.email_usuario], fail_silently=False)

# --- NOVA CONFIGURAÇÃO PARA DADOS EMPRESARIAIS ---
@admin.register(DadosEmpresariais)
class DadosEmpresariaisAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'cnpj', 'nome_responsavel', 'status', 'data_atualizacao')
    list_filter = ('status', 'data_atualizacao')
    search_fields = ('nome_fantasia', 'razao_social', 'cnpj', 'nome_responsavel')
    readonly_fields = ('data_criacao', 'data_atualizacao')
    
    actions = ['aprovar_cadastro']

    # Organiza o formulário de edição em abas, espelhando o formulário do usuário
    fieldsets = (
        ('Status do Cadastro', {
            'fields': ('status',)
        }),
        ('Etapa 1: Dados da Empresa', {
            'fields': ('nome_fantasia', 'razao_social', 'cnpj', 'inscricao_estadual', 'atividade_principal', 'atividades_secundarias', 'documento_comprobatorio_empresa')
        }),
        ('Etapa 2: Dados do Responsável Legal/Delegado', {
            'fields': ('nome_responsavel', 'cpf_responsavel', 'cargo_responsavel', 'email_responsavel', 'telefone_responsavel', 'documento_vinculo_responsavel')
        }),
        ('Etapa 3: Dados Complementares', {
            'fields': ('endereco', 'telefone_institucional', 'email_institucional', 'website', 'apresentacao_empresa')
        }),
        ('Datas de Controle', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',) # Começa recolhido
        }),
    )

    @admin.action(description='Mudar status para "Aprovado"')
    def aprovar_cadastro(self, request, queryset):
        queryset.update(status='APROVADO')
        self.message_user(request, "Os cadastros selecionados foram APROVADOS com sucesso.")