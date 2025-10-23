from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CandidatoCadastroForm # Importa o formulário que acabamos de criar
from .models import Usuario, Candidato
from django.db import transaction # Garante que os dois models sejam criados com segurança
from django.contrib import messages
from django.http import HttpResponse

@transaction.atomic # Garante que ou os dois são criados, ou nenhum é
def cadastrar_candidato(request):
    """
    Processa o formulário de cadastro do UC01.
    """
    if request.method == 'POST':
        form = CandidatoCadastroForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            
            # 1. Cria o Usuario (Portaria) 
            # Usamos o email como username, como discutido
            user = Usuario.objects.create_user(
                username=data['email'], # Usa email como username
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                telefone=data['telefone'],
                tipo_usuario='candidato'
            )
            
            # 2. Cria o Candidato (Sala) 
            candidato = Candidato.objects.create(
                usuario=user, # Conecta o perfil ao login
                cpf=data['cpf']
            )
            
            # 3. Loga o usuário automaticamente após o cadastro
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            # Redireciona para o painel do candidato (vamos criar essa URL depois)
            return redirect('home_candidato') # 
    
    else:
        # Se for um GET (usuário só abriu a página), mostra um form vazio [cite: 11]
        form = CandidatoCadastroForm()
        
    # Renderiza a página HTML, passando o formulário para ela
    return render(request, 'usuarios/cadastro_candidato.html', {'form': form})

def login_view(request):
    """
    Processa a página de login para Candidatos e Recrutadores (UC03).
    """
    if request.method == 'POST':
        # No HTML, o <input> deve ter name="username"
        login_identifier = request.POST.get('username')
        password = request.POST.get('password')

        # O 'authenticate' agora usa nosso EmailOrCPFBackend
        user = authenticate(request, username=login_identifier, password=password)

        if user is not None:
            # Login foi bem-sucedido!
            login(request, user)
            
            # --- TAREFA: CONTROLE DE PERMISSÕES ---
            # Aqui checamos o "crachá" (tipo_usuario)
            if user.tipo_usuario == 'candidato':
                return redirect('home_candidato') # Redireciona para o painel do candidato
            elif user.tipo_usuario == 'recrutador':
                return redirect('home_recrutador') # Redireciona para o painel da empresa
            
            return redirect('pagina_padrao') # Uma página genérica
        else:
            # Login falhou, conforme UC03
            messages.error(request, 'Credenciais inválidas. Por favor, tente novamente.')
            
    # Se for um GET ou se o login falhar, mostra a página de login
    return render(request, 'usuarios/login.html')

def logout_view(request):
    """
    Faz o logout do usuário e o redireciona para a tela de login.
    """
    logout(request)
    return redirect('login') # Redireciona para a URL da página de login

def home_candidato(request):
    # Esta é a view temporária para o painel do candidato
    # Mais tarde, vamos substituí-la por um template real
    return HttpResponse("<h1>Você está logado como CANDIDATO</h1>")

def home_recrutador(request):
    # Esta é a view temporária para o painel do recrutador
    return HttpResponse("<h1>Você está logado como RECRUTADOR</h1>")