# Arquivo: apps/usuarios/urls.py

from django.urls import path
from . import views  # Importa as views do app (views.py)

urlpatterns = [
    # URL para a página de login
    path('login/', views.login_view, name='login'),

    # URL para o processo de logout
    path('logout/', views.logout_view, name='logout'),

    # URL para a página de cadastro de candidato
    path('cadastro/candidato/', views.cadastrar_candidato, name='cadastro_candidato'),

    # (Mais tarde, adicionaremos o cadastro da empresa aqui)
    # path('cadastro/empresa/', views.cadastrar_empresa, name='cadastro_empresa'),

    # URLs de placeholder para os painéis
    path('dashboard/candidato/', views.home_candidato, name='home_candidato'),
    path('dashboard/recrutador/', views.home_recrutador, name='home_recrutador'),
]