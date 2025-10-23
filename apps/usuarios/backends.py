from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import Candidato # Precisamos checar o CPF na tabela Candidato

UserModel = get_user_model() # Pega o seu modelo 'Usuario' customizado

class EmailOrCPFBackend(ModelBackend):
    """
    Autentica um usuário usando seu email ou CPF, conforme UC03.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        
        # O campo 'username' do formulário HTML virá com o "Email/CPF"
        login_identifier = username 
        
        try:
            # 1. Tentar encontrar o usuário pelo E-mail (ignora maiúscula/minúscula)
            user = UserModel.objects.get(email__iexact=login_identifier)
        except UserModel.DoesNotExist:
            try:
                # 2. Se não achou por email, tentar encontrar pelo CPF
                # Remove pontos/traços do CPF digitado
                cpf_digits = ''.join(filter(str.isdigit, login_identifier))
                if len(cpf_digits) == 11:
                    candidato = Candidato.objects.get(cpf=cpf_digits)
                    user = candidato.usuario # Se achou o perfil, pega o usuário principal
                else:
                    user = None
            except Candidato.DoesNotExist:
                user = None # Nenhum usuário encontrado

        # 3. Se um usuário foi encontrado (por email ou CPF), checa a senha
        if user:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user # Login com sucesso!
        
        # Se não encontrou ou a senha está errada
        return None

    def get_user(self, user_id):
        # Função padrão do Django para buscar o usuário após o login
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None