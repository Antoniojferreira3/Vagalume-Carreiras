# Arquivo: apps/usuarios/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, Empresa, Candidato, Recrutador, 
    Resumo_Profissional, Idiomas, Redes_Sociais, 
    Skill, Experiencia, Formacao_Academica
)

# --- Inlines para o Perfil do Candidato ---
# Permitem editar os modelos relacionados na mesma tela do Candidato

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1  # Mostrar 1 campo em branco para adicionar nova skill

class ExperienciaInline(admin.StackedInline):
    model = Experiencia
    extra = 0 # Não mostrar campos em branco por padrão

class FormacaoAcademicaInline(admin.StackedInline):
    model = Formacao_Academica
    extra = 0

class ResumoProfissionalInline(admin.StackedInline):
    model = Resumo_Profissional
    max_num = 1 # Um candidato só pode ter um resumo

class IdiomasInline(admin.TabularInline):
    model = Idiomas
    extra = 0

class RedesSociaisInline(admin.TabularInline):
    model = Redes_Sociais
    extra = 0


# --- Configurações Principais do Admin ---

class CustomUserAdmin(UserAdmin):
    model = Usuario
    # Adiciona os campos customizados ('tipo_usuario', 'telefone') no admin
    fieldsets = UserAdmin.fieldsets + (
        ('Campos Personalizados', {'fields': ('tipo_usuario', 'telefone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Campos Personalizados', {'fields': ('tipo_usuario', 'telefone')}),
    )
    list_display = ('email', 'username', 'first_name', 'last_name', 'tipo_usuario', 'is_staff')
    list_filter = ('tipo_usuario', 'is_staff', 'is_active')

@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'get_nome_completo', 'cpf', 'headline')
    search_fields = ('cpf', 'headline', 'usuario__email', 'usuario__first_name', 'usuario__last_name')
    
    # Adiciona os inlines na página de detalhes do Candidato
    inlines = [
        ResumoProfissionalInline,
        ExperienciaInline,
        FormacaoAcademicaInline,
        SkillInline,
        IdiomasInline,
        RedesSociaisInline,
    ]

    # Funções para mostrar dados do modelo Usuario na lista
    def get_email(self, obj):
        return obj.usuario.email
    get_email.short_description = 'Email'

    def get_nome_completo(self, obj):
        return obj.usuario.get_full_name()
    get_nome_completo.short_description = 'Nome Completo'

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'setor', 'telefone')
    search_fields = ('nome', 'cnpj', 'setor')

@admin.register(Recrutador)
class RecrutadorAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'empresa', 'get_nome_usuario')
    search_fields = ('usuario__email', 'empresa__nome')
    raw_id_fields = ('empresa', 'usuario') # Melhora performance para selecionar FKs
    list_filter = ('empresa',)

    def get_email(self, obj):
        return obj.usuario.email
    get_email.short_description = 'Email do Recrutador'

    def get_nome_usuario(self, obj):
        return obj.usuario.get_full_name()
    get_nome_usuario.short_description = 'Nome'

# --- Registro dos Modelos ---

# Desregistra o usuário padrão se já estiver registrado (raro, mas garante)
# admin.site.unregister(Usuario) # Descomente se der erro de "já registrado"
admin.site.register(Usuario, CustomUserAdmin)

# Os modelos abaixo não são mais registrados aqui, 
# pois são gerenciados pelos Inlines do CandidatoAdmin:
# Resumo_Profissional, Idiomas, Redes_Sociais, 
# Skill, Experiencia, Formacao_Academica

# Os modelos abaixo já estão registrados com @admin.register:
# Empresa, Candidato, Recrutador