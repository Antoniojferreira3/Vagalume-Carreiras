from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, Empresa, Candidato, Recrutador, 
    Resumo_Profissional, Idiomas, Redes_Sociais, 
    Skill, Experiencia, Formacao_Academica
)

# --- Inlines para o Candidato ---
# Estes permitem editar experiências/skills DENTRO da página do Candidato
class ExperienciaInline(admin.TabularInline): # Ou admin.StackedInline
    model = Experiencia
    extra = 1 # Quantos campos em branco mostrar

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1

class Formacao_AcademicaInline(admin.TabularInline):
    model = Formacao_Academica
    extra = 1
# ... (você pode criar inlines para todos)

# --- Admin do Candidato ---
class CandidatoAdmin(admin.ModelAdmin):
    inlines = [
        ExperienciaInline,
        SkillInline,
        Formacao_AcademicaInline,
        # ... outros inlines
    ]

# --- Admin do Usuário ---
class CustomUserAdmin(UserAdmin):
    model = Usuario
    # ... (seu código que já está correto) ...

# --- Registros ---
admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Empresa)
admin.site.register(Candidato, CandidatoAdmin) # Registra o Candidato com os inlines
admin.site.register(Recrutador)

# Não precisa registrar os modelos que já estão como 'inline', 
# mas se quiser que eles tenham sua própria página, pode manter.
# admin.site.register(Skill) 
# admin.site.register(Experiencia)
# ...