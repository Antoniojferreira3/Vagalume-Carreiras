from django.db import models
from apps.usuarios.models import Candidato, Empresa, Recrutador

class Vaga(models.Model):
    # Conecta a Vaga à Empresa que a publicou
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    # Conecta a Vaga ao Recrutador que a criou
    recrutador = models.ForeignKey(Recrutador, on_delete=models.CASCADE)

    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    requisitos = models.TextField()
    tipo_contrato = models.CharField(max_length=50)
    localidade = models.CharField(max_length=100)
    beneficios = models.TextField(blank=True, null=True)
    faixa_salarial = models.CharField(max_length=50, blank=True, null=True)
    status = models.BooleanField(default=True) # True = Aberta, False = Fechada
    data_publicacao = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Candidatura(models.Model):
    # Esta é a tabela que LIGA o Candidato e a Vaga
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)

    data_candidatura = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Enviada') # Ex: 'Enviada', 'Em análise', etc.
    
    class Meta:
        # Garante que um candidato não possa se aplicar 2x na mesma vaga
        unique_together = ('candidato', 'vaga')