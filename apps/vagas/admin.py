# Arquivo: apps/vagas/admin.py

from django.contrib import admin
from .models import Vaga, Candidatura

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'empresa', 'localidade', 'tipo_contrato', 'status', 'data_publicacao')
    list_filter = ('status', 'tipo_contrato', 'localidade', 'empresa')
    search_fields = ('titulo', 'descricao', 'requisitos', 'empresa__nome')
    date_hierarchy = 'data_publicacao' # Adiciona navegação por data
    ordering = ('-data_publicacao',)
    
    # Permite mudar o status (True/False) direto na lista
    list_editable = ('status',)
    
    # Melhora a performance de seleção de FKs com muitos itens
    raw_id_fields = ('empresa', 'recrutador')

@admin.register(Candidatura)
class CandidaturaAdmin(admin.ModelAdmin):
    list_display = ('vaga', 'candidato', 'data_candidatura', 'status')
    list_filter = ('status', 'data_candidatura', 'vaga__empresa')
    search_fields = ('vaga__titulo', 'candidato__usuario__email', 'candidato__usuario__first_name')
    date_hierarchy = 'data_candidatura'
    ordering = ('-data_candidatura',)
    
    # Melhora a performance
    raw_id_fields = ('candidato', 'vaga')