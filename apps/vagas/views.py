from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required # Importa o decorador de login
from django.contrib import messages
from .models import Vaga, Candidatura
from .forms import VagaForm
from apps.usuarios.models import Recrutador # Precisamos saber quem é o recrutador
from django.http import HttpResponse

@login_required # 1. Garante que o usuário DEVE estar logado para acessar
def criar_vaga(request):
    """
    View para um Recrutador criar uma nova vaga.
    """
    # 2. CONTROLE DE PERMISSÃO:
    # Verifica se o "crachá" do usuário é de recrutador
    if request.user.tipo_usuario != 'recrutador':
        messages.error(request, 'Acesso negado. Esta página é apenas para recrutadores.')
        return redirect('home_candidato') # Redireciona para uma página inicial genérica

    if request.method == 'POST':
        form = VagaForm(request.POST)
        
        if form.is_valid():
            # Não salva no banco ainda, precisamos adicionar o dono da vaga
            vaga = form.save(commit=False)
            
            # 3. CONECTA A VAGA AO SEU DONO
            # Pega o perfil do recrutador logado
            recrutador_logado = get_object_or_404(Recrutador, usuario=request.user)
            vaga.recrutador = recrutador_logado
            vaga.empresa = recrutador_logado.empresa # Pega a empresa do recrutador
            
            vaga.save() # Agora sim, salva no banco
            
            messages.success(request, 'Vaga criada com sucesso!')
            return redirect('home_recrutador') # Redireciona para o painel do recrutador
    else:
        # Se for um GET, apenas mostra o formulário vazio
        form = VagaForm()
        return render(request, 'vagas/criar_vaga.html', {'form': form})
    
def home_candidato(request):
    # Esta é a view temporária para o painel do candidato
    return HttpResponse("<h1>Painel do Candidato</h1><p>Em breve, aqui você verá as vagas.</p>")

def home_recrutador(request):
    # Esta é a view temporária para o painel do recrutador
    return HttpResponse("<h1>Painel do Recrutador</h1><p>Em breve, aqui você verá suas vagas criadas.</p>")

    