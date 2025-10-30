# Arquivo: apps/usuarios/urls.py

from django.urls import path
from . import views 

urlpatterns = [
    # URLs de Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # URLs de Cadastro
    path('cadastro/candidato/', views.cadastrar_candidato, name='cadastro_candidato'),
    # --- NOVA URL ---
    path('cadastro/recrutador/', views.cadastrar_recrutador, name='cadastro_recrutador'),

    # URLs dos Painéis (Dashboards)
    path('dashboard/candidato/', views.home_candidato, name='home_candidato'),
    path('dashboard/recrutador/', views.home_recrutador, name='home_recrutador'),
]