from django.db import models

class Candidato(models.Model):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=255)
    email = models.EmailField(max_length=50, unique=True)
    senha = models.CharField(max_length=255) # Em um projeto real, usaríamos o sistema de usuários do Django
    telefone = models.CharField(max_length=15, blank=True, null=True) # blank=True permite campo vazio no admin
    cpf = models.CharField(max_length=11, unique=True)
    headline = models.CharField(max_length=255, blank=True, null=True)
    resumo_profissional = models.TextField(blank=True, null=True)
    hard_skills = models.TextField(blank=True, null=True)
    soft_skills = models.TextField(blank=True, null=True)

class Idiomas(models.Model):
    idioma = models.CharField(max_length=50)
    nivel = models.CharField(max_length=50)

class Redes_Sociais(models.Model):
    tipo_rede = models.CharField(max_length=50)
    link = models.URLField(max_length=200)

class Skill(models.Model):
    hard_skill = models.CharField(max_length=100)
    soft_skill = models.CharField(max_length=100)

class Resumo_Profissional(models.Model):
    texto = models.TextField(max_length=500)

class Experiencia(models.Model):
    cargo = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    trabalha_atualmente = models.BooleanField(default=False)
    descricao = models.TextField(blank=True, null=True)

class Candidatura(models.Model):
    data_candidatura = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50)

class Formacao_Academica(models.Model):
    nome_instituicao = models.CharField(max_length=100)
    nome_formacao = models.CharField(max_length=100)
    nivel = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    formacao_exterior = models.BooleanField(default=False)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    cursando_atualmente = models.BooleanField(default=False)

class Vaga(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    requisitos = models.TextField()
    tipo_contrato = models.CharField(max_length=50)
    localidade = models.CharField(max_length=100)
    beneficios = models.TextField(blank=True, null=True)
    faixa_salarial = models.CharField(max_length=50, blank=True, null=True)
    status = models.BooleanField(default=True)
    data_publicacao = models.DateField(auto_now_add=True)

class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, unique=True)
    senha = models.CharField(max_length=255) 
    telefone = models.CharField(max_length=15, blank=True, null=True)
    cnpj = models.CharField(max_length=14, unique=True)
    setor = models.CharField(max_length=100)

class Recrutador(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, unique=True)
    senha = models.CharField(max_length=255)

class Administrador(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, unique=True)
    senha = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"