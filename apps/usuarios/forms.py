from django import forms
from .models import Usuario, Candidato
import re # Para limpar o CPF

class CandidatoCadastroForm(forms.Form):
    """
    Formulário para o fluxo UC01: Cadastrar Novo Candidato.
    Coleta dados para os models Usuario e Candidato.
    """
    
    # Campos do seu design no Figma
    first_name = forms.CharField(label='Nome', max_length=100)
    last_name = forms.CharField(label='Sobrenome', max_length=100)
    email = forms.EmailField(label='Email')
    telefone = forms.CharField(label='Telefone', max_length=20)
    cpf = forms.CharField(label='CPF', max_length=14) # Permite máscaras (ex: 123.456.789-00)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput)

    def clean_cpf(self):
        # Validação do CPF 
        cpf = self.cleaned_data.get('cpf')
        cpf_digits = re.sub(r'[^0-9]', '', cpf) # Remove pontos e traços
        
        if len(cpf_digits) != 11:
            raise forms.ValidationError("CPF deve conter 11 dígitos.")
        
        # Validação de unicidade
        if Candidato.objects.filter(cpf=cpf_digits).exists():
            raise forms.ValidationError("Este CPF já está cadastrado. Tente fazer login.")
        
        return cpf_digits # Retorna o CPF limpo

    def clean_email(self):
        # Validação de unicidade do Email
        email = self.cleaned_data.get('email').lower()
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está cadastrado. Tente fazer login.") 
        return email

    def clean(self):
        # Validação para checar se as senhas coincidem [cite: 19]
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("As senhas não coincidem.")
        
        return cleaned_data