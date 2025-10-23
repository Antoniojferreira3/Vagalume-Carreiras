# Arquivo: vagalume_carreiras/urls.py

from django.contrib import admin
from django.urls import path, include  # <-- 1. Adicione o 'include'

urlpatterns = [
    path('admin/', admin.site.urls),

    # 2. Adicione esta linha:
    # Ela diz ao Django: "Qualquer URL que comece com 'contas/'...
    # ...deve ser gerenciada pelo nosso arquivo 'apps.usuarios.urls'".
    path('contas/', include('apps.usuarios.urls')),

    # (Mais tarde, faremos o mesmo para o app de vagas)
    # path('', include('apps.vagas.urls')),
]