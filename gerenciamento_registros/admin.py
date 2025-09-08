# Arquivo: gerenciamento_registros/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, PermissionarioProfile, AprendizProfile, ModeloEmail

# Define um 'inline' para o perfil de permissionário.
# Isso permite editar o órgão/lotação na mesma tela de edição do usuário.
class PermissionarioProfileInline(admin.StackedInline):
    model = PermissionarioProfile
    can_delete = False
    verbose_name_plural = 'Perfil de Permissionário'

# Define um 'inline' para o perfil de aprendiz.
class AprendizProfileInline(admin.StackedInline):
    model = AprendizProfile
    can_delete = False
    verbose_name_plural = 'Perfil de Aprendiz'

# Define a área de administração para o nosso CustomUser
class CustomUserAdmin(UserAdmin):
    # Adiciona 'tipo_usuario' aos campos exibidos na lista
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'tipo_usuario')
    list_filter = UserAdmin.list_filter + ('tipo_usuario',)

    # Adiciona os campos customizados à tela de edição do usuário
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo_usuario', 'is_email_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo_usuario', 'is_email_verified')}),
    )

    inlines = [PermissionarioProfileInline, AprendizProfileInline]

    # Lógica para mostrar os perfis 'inline' apenas para o tipo de usuário correto
    def get_inlines(self, request, obj=None):
        if obj:
            if obj.tipo_usuario == 'PERMISSIONARIO':
                return [PermissionarioProfileInline]
            if obj.tipo_usuario == 'APRENDIZ':
                return [AprendizProfileInline]
        return []

# Define a área de administração para os Modelos de E-mail
@admin.register(ModeloEmail)
class ModeloEmailAdmin(admin.ModelAdmin):
    list_display = ('identificador', 'assunto')
    search_fields = ('identificador', 'assunto')


# Registra nosso CustomUser com a configuração customizada
admin.site.register(CustomUser, CustomUserAdmin)