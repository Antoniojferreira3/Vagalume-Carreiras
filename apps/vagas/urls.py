# Arquivo: apps/vagas/urls.py

from django.urls import path
from . import views  # Importa as views do app (views.py)

urlpatterns = [
    # URL para a página de criar vaga
    path('vagas/criar/', views.criar_vaga, name='criar_vaga'),

    # URLs de placeholder para os painéis
    # Estamos colocando os painéis principais aqui
    path('dashboard/candidato/', views.home_candidato, name='home_candidato'),
    path('dashboard/recrutador/', views.home_recrutador, name='home_recrutador'),
]