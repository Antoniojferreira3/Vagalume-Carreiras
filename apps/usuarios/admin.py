from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, Empresa, Candidato, Recrutador, 
    Resumo_Profissional, Idiomas, Redes_Sociais, 
    Skill, Experiencia, Formacao_Academica
)

# Para customizar a exibição do seu Usuário no admin
class CustomUserAdmin(UserAdmin):
    model = Usuario
    # Adiciona os campos customizados ('tipo_usuario', 'telefone') no admin
    fieldsets = UserAdmin.fieldsets + (
        ('Campos Personalizados', {'fields': ('tipo_usuario', 'telefone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Campos Personalizados', {'fields': ('tipo_usuario', 'telefone')}),
    )

# Registra o Usuário com a visualização customizada
admin.site.register(Usuario, CustomUserAdmin)

# Registra todos os outros perfis e modelos
admin.site.register(Empresa)
admin.site.register(Candidato)
admin.site.register(Recrutador)
admin.site.register(Resumo_Profissional)
admin.site.register(Idiomas)
admin.site.register(Redes_Sociais)
admin.site.register(Skill)
admin.site.register(Experiencia)
admin.site.register(Formacao_Academica)