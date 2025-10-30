# apps/usuarios/forms.py

from django import forms
from django.db import transaction
from .models import Usuario, Candidato, Empresa, Recrutador
import re # Para limpar o CPF e CNPJ

# -------------------------------------------------------------------
# FORMULÁRIO DE CADASTRO DO CANDIDATO (UC01)
# -------------------------------------------------------------------
class CandidatoCadastroForm(forms.Form):
    """
    Formulário para o fluxo UC01: Cadastrar Novo Candidato.
    Coleta dados para os models Usuario e Candidato.
    """
    
    # Campos do Usuario
    first_name = forms.CharField(label='Nome', max_length=100)
    last_name = forms.CharField(label='Sobrenome', max_length=100)
    email = forms.EmailField(label='Email')
    telefone = forms.CharField(label='Telefone', max_length=20, required=False)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput)
    
    # Campo do Candidato
    cpf = forms.CharField(label='CPF', max_length=14) # Permite máscaras (ex: 123.456.789-00)

    # --- MÉTODOS DE VALIDAÇÃO (DENTRO DA CLASSE) ---

    def clean_cpf(self):
        """ Validação e limpeza do CPF """
        cpf = self.cleaned_data.get('cpf')
        cpf_digits = re.sub(r'[^0-9]', '', cpf) # Remove pontos e traços
        
        if len(cpf_digits) != 11:
            raise forms.ValidationError("CPF deve conter 11 dígitos.")
        
        if Candidato.objects.filter(cpf=cpf_digits).exists():
            raise forms.ValidationError("Este CPF já está cadastrado. Tente fazer login.")
        
        return cpf_digits # Retorna o CPF limpo

    def clean_email(self):
        """ Validação de unicidade do Email """
        email = self.cleaned_data.get('email').lower()
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está cadastrado. Tente fazer login.") 
        return email

    def clean(self):
        """ Validação para checar se as senhas coincidem """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            # Coloca o erro no campo 'password_confirm' para aparecer abaixo dele
            self.add_error('password_confirm', "As senhas não coincidem.")
        
        return cleaned_data

    @transaction.atomic # Garante que ou tudo é criado, ou nada é
    def save(self):
        """
        Cria o Usuario e o Candidato em uma única transação.
        Este método é chamado lá na views.py (view cadastrar_candidato)
        """
        data = self.cleaned_data
        
        # 1. Cria o Usuario (Portaria)
        user = Usuario.objects.create_user(
            username=data['email'], # Usa email como username
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            telefone=data['telefone'],
            tipo_usuario='candidato' # Define o tipo
        )
        
        # 2. Cria o Candidato (Sala)
        candidato = Candidato.objects.create(
            usuario=user, # Conecta o login
            cpf=data['cpf']
            # NOTA: O 'headline' é opcional e pode ser preenchido depois
        )
        
        return user # Retorna o usuário criado para o login
    # -------------------------------------------------------------------
# FORMULÁRIO DE CADASTRO DA EMPRESA E RECRUTADOR (UC02)
# -------------------------------------------------------------------
class RecrutadorCadastroForm(forms.Form):
    """
    Formulário para o fluxo UC02: Cadastrar Nova Empresa/Recrutador.
    Coleta dados para os models Empresa, Usuario e Recrutador.
    """
    
    # Campos da Empresa
    nome_empresa = forms.CharField(label='Nome da Empresa', max_length=150)
    cnpj = forms.CharField(label='CNPJ', max_length=18) # Permite máscaras (ex: 12.345.678/0001-90)

    # Campos do Usuario (Recrutador)
    first_name = forms.CharField(label='Nome (Recrutador)', max_length=100)
    last_name = forms.CharField(label='Sobrenome (Recrutador)', max_length=100)
    email = forms.EmailField(label='Email (será seu login)')
    telefone = forms.CharField(label='Telefone', max_length=20, required=False)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput)

    # --- MÉTODOS DE VALIDAÇÃO (DENTRO DA CLASSE) ---

    def clean_cnpj(self):
        """ Validação e limpeza do CNPJ """
        cnpj = self.cleaned_data.get('cnpj')
        cnpj_digits = re.sub(r'[^0-9]', '', cnpj) # Remove pontos, traços e barras
        
        if len(cnpj_digits) != 14:
            raise forms.ValidationError("CNPJ deve conter 14 dígitos.")
        
        if Empresa.objects.filter(cnpj=cnpj_digits).exists():
            raise forms.ValidationError("Este CNPJ já está cadastrado.")
        
        return cnpj_digits # Retorna o CNPJ limpo

    def clean_email(self):
        """ Validação de unicidade do Email """
        email = self.cleaned_data.get('email').lower()
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está cadastrado. Tente fazer login.") 
        return email

    def clean(self):
        """ Validação para checar se as senhas coincidem """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "As senhas não coincidem.")
        
        return cleaned_data

    @transaction.atomic # Garante que ou tudo é criado, ou nada é
    def save(self):
        """
        Cria a Empresa, o Usuario e o Recrutador em uma única transação.
        Este método é chamado lá na views.py (view cadastrar_recrutador)
        """
        data = self.cleaned_data
        
        # 1. Cria a Empresa
        empresa = Empresa.objects.create(
            nome=data['nome_empresa'],
            cnpj=data['cnpj']
            # NOTA: Outros campos da empresa (descricao, site) são opcionais
        )

        # 2. Cria o Usuario (Portaria) para o Recrutador
        user = Usuario.objects.create_user(
            username=data['email'], # Usa email como username
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            telefone=data['telefone'],
            tipo_usuario='recrutador' # Define o tipo
        )
        
        # 3. Cria o Recrutador (Sala)
        recrutador = Recrutador.objects.create(
            usuario=user, # Conecta o login
            empresa=empresa # Conecta o recrutador à empresa que acabamos de criar
            # NOTA: O 'cargo' é opcional e pode ser preenchido depois
        )
        
        return user # Retorna o usuário criado para o login