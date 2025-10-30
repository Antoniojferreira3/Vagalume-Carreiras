from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
# Importa OS DOIS formulários
from .forms import CandidatoCadastroForm, RecrutadorCadastroForm 
# Importa OS TRÊS modelos de perfil
from .models import Usuario, Candidato, Empresa, Recrutador
from django.db import transaction 
from django.contrib import messages
from django.http import HttpResponse

# --- Importa os novos decorators ---
from .decorators import candidato_required, recrutador_required, anonymous_required
from django.contrib.auth.decorators import login_required # Decorator padrão do Django


@anonymous_required 
@transaction.atomic 
def cadastrar_candidato(request):
    """
    Processa o formulário de cadastro do UC01.
    """
    if request.method == 'POST':
        form = CandidatoCadastroForm(request.POST)
        
        if form.is_valid():
            # AGORA a lógica de salvar está DENTRO do form.save()
            # Esta linha 'user = form.save()' executa aquele método .save()
            # que nós criamos dentro da classe CandidatoCadastroForm
            user = form.save() 
            
            # 3. Loga o usuário automaticamente
            login(request, user, backend='django.contrib.auth.backends.ModelBackend') 
            
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('home_candidato')
    
    else:
        form = CandidatoCadastroForm()
        
    return render(request, 'usuarios/cadastro_candidato.html', {'form': form})

# --- NOVA VIEW PARA O RECRUTADOR ---
@anonymous_required # Protege contra usuários já logados
@transaction.atomic
def cadastrar_recrutador(request):
    """
    Processa o formulário de cadastro do Recrutador.
    """
    if request.method == 'POST':
        form = RecrutadorCadastroForm(request.POST)
        
        if form.is_valid():
            # O método .save() do formulário já cria os 3 objetos
            user = form.save() 
            
            # Loga o usuário automaticamente
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            messages.success(request, 'Cadastro realizado com sucesso! Sua empresa agora está em nossa plataforma.')
            return redirect('home_recrutador')
    
    else:
        form = RecrutadorCadastroForm()
        
    return render(request, 'usuarios/cadastro_recrutador.html', {'form': form})


@anonymous_required # Protege contra usuários já logados
def login_view(request):
    """
    Processa a página de login para Candidatos e Recrutadores (UC03).
    """
    if request.method == 'POST':
        login_identifier = request.POST.get('username') # 'username' é o name="" do input
        password = request.POST.get('password')

        # O 'authenticate' agora usa nosso EmailOrCPFBackend (se configurado no settings.py)
        user = authenticate(request, username=login_identifier, password=password)

        if user is not None:
            login(request, user)
            
            # --- Controle de Permissões no Login ---
            if user.tipo_usuario == 'candidato':
                return redirect('home_candidato') 
            elif user.tipo_usuario == 'recrutador':
                return redirect('home_recrutador') 
            
            # Se for um admin (sem tipo), redireciona para o admin
            elif user.is_staff:
                return redirect('/admin/') # URL padrão do admin
            
            return redirect('login') # Fallback
        else:
            messages.error(request, 'Credenciais inválidas. Por favor, tente novamente.')
            
    return render(request, 'usuarios/login.html')

@login_required # Só pode fazer logout se estiver logado
def logout_view(request):
    """
    Faz o logout do usuário e o redireciona para a tela de login.
    """
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('login') 


# --- PROTEGENDO AS VIEWS DO PAINEL ---

@login_required # Requer login
@candidato_required # Requer que o tipo seja 'candidato'
def home_candidato(request):
    return render(request, 'dashboard/home_candidato.html') # Mudei para um template real

@login_required # Requer login
@recrutador_required # Requer que o tipo seja 'recrutador'
def home_recrutador(request):
    return render(request, 'dashboard/home_recrutador.html') # Mudei para um template real