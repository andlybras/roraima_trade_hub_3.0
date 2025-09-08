from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, PermissionarioProfile, AprendizProfile, ModeloEmail

class PermissionarioProfileInline(admin.StackedInline):
    model = PermissionarioProfile
    can_delete = False
    verbose_name_plural = 'Perfil de Permissionário'

class AprendizProfileInline(admin.StackedInline):
    model = AprendizProfile
    can_delete = False
    verbose_name_plural = 'Perfil de Aprendiz'

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'tipo_usuario')
    list_filter = UserAdmin.list_filter + ('tipo_usuario',)
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo_usuario', 'is_email_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo_usuario', 'is_email_verified')}),
    )
    inlines = [PermissionarioProfileInline, AprendizProfileInline]

    def get_inlines(self, request, obj=None):
        if obj:
            if obj.tipo_usuario == 'PERMISSIONARIO':
                return [PermissionarioProfileInline]
            if obj.tipo_usuario == 'APRENDIZ':
                return [AprendizProfileInline]
        return []

@admin.register(ModeloEmail)
class ModeloEmailAdmin(admin.ModelAdmin):
    list_display = ('identificador', 'assunto')
    search_fields = ('identificador', 'assunto')

admin.site.register(CustomUser, CustomUserAdmin)