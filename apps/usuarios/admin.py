from django.contrib import admin
from .models import Candidato, Empresa, Recrutador, Experiencia # Importe todos os models deste app

# Registra os models para que apareçam na área de admin
admin.site.register(Candidato)
admin.site.register(Empresa)
admin.site.register(Recrutador)
admin.site.register(Experiencia)
# Faça isso para todos os models que você quer ver