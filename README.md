Manual de Instalação — Plataforma de Vagas e Recrutamento Inteligente ( Vagalume Carreiras )


1. Requisitos do Sistema

Antes de iniciar, verifique se o ambiente possui:
Python 3.10+
PostgreSQL 14+
Git
Pip e venv
(Opcional) Visual Studio Code ou outro editor de texto

2. Clonar o Repositório

Abra o terminal e execute:
git clone https://github.com/pedroH901/Vagalume-Carreiras.git
Em seguida, acesse a pasta do projeto:
cd vagalume-carreiras

3. Criar e Ativar o Ambiente Virtual
No terminal:
python -m venv venv
Ativar o ambiente:
Windows
venv\Scripts\activate
Linux/Mac
source venv/bin/activate

4. Instalar as Dependências
Execute:
pip install -r requirements.txt
Caso o arquivo requirements.txt ainda não exista, gere com:
pip freeze > requirements.txt

Principais dependências:
Django
djangorestframework
django-crispy-forms
django-filter
psycopg2
pillow
scikit-learn
nltk

5. Configurar o Banco de Dados PostgreSQL

Crie um banco de dados:
CREATE DATABASE vagalume-carreiras;
No arquivo settings.py, localize a configuração de banco:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'plataforma_vagas',
        'USER': 'postgres',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

6. Executar as Migrações
Crie as tabelas no banco:
python manage.py makemigrations
python manage.py migrate

7. Criar Usuário Administrador
python manage.py createsuperuser
Preencha com e-mail, nome e senha.

8. Rodar o Servidor
python manage.py runserver
Acesse no navegador:
http://127.0.0.1:8000/

9. Testar a Aplicação
Login: /admin/
API REST (exemplo): /api/vagas/
Frontend: página inicial ou diretório /templates/

10. Erros Comuns                          
Erro - psycopg2.OperationalError
Solução - Verifique se o PostgreSQL está rodando e as credenciais no settings.py.

Erro - ModuleNotFoundError	        
Solução - Execute pip install -r requirements.txt novamente.

Erro - DisallowedHost	                
Solução - Adicione localhost em ALLOWED_HOSTS no settings.py.


11. Estrutura de Pastas (Exemplo)
vagalumne-carreiras/
│
├── manage.py
├── requirements.txt
├── db.sqlite3 (opcional)
│
├── core/               # app principal (usuários, autenticação)
├── vagas/              # app de vagas e candidaturas
├── matching/           # app com algoritmo de matching
├── api/                # app REST
└── templates/          # páginas HTML

12. Desativar o Ambiente Virtual
Quando terminar o trabalho:
deactivate

13. (Opcional) Implantação
Para publicação online (exemplo):
Render, Railway, ou PythonAnywhere
Banco: PostgreSQL hospedado
Variáveis de ambiente configuradas (.env)
