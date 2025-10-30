from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def user_type_required(user_type, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator que verifica se o usuário logado tem o 'tipo_usuario' correto.
    """
    def decorator(view_func):
        @user_passes_test(
            lambda u: u.is_authenticated and u.tipo_usuario == user_type,
            login_url=login_url,
            redirect_field_name=redirect_field_name
        )
        def _wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# --- Decorators Prontos para Usar ---

# Protege views que só podem ser acessadas por Candidatos
candidato_required = user_type_required('candidato', login_url='login')

# Protege views que só podem ser acessadas por Recrutadores
recrutador_required = user_type_required('recrutador', login_url='login')

# Proteção extra: Redireciona usuários já logados da página de login/cadastro
def anonymous_required(view_func):
    """
    Decorator para views que não devem ser acessadas por usuários já logados
    (ex: página de login ou cadastro).
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redireciona baseado no tipo de usuário
            if request.user.tipo_usuario == 'candidato':
                return redirect('home_candidato')
            elif request.user.tipo_usuario == 'recrutador':
                return redirect('home_recrutador')
            else:
                return redirect('login') # Fallback
        return view_func(request, *args, **kwargs)
    return _wrapped_view