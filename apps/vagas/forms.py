# Arquivo: apps/vagas/forms.py

from django import forms
from .models import Vaga

class VagaForm(forms.ModelForm):
    """
    Formulário para o Recrutador criar ou editar uma Vaga.
    """
    class Meta:
        model = Vaga # O formulário será baseado no seu model Vaga
        
        # Lista de campos do seu model que aparecerão no formulário
        fields = [
            'titulo', 
            'descricao', 
            'requisitos', 
            'tipo_contrato', 
            'localidade', 
            'beneficios', 
            'faixa_salarial',
            'status', # (True = Aberta, False = Fechada)
        ]

    def __init__(self, *args, **kwargs):
        # Este __init__ é só para deixar o form mais bonito (adiciona classes do Bootstrap, por ex.)
        # É opcional, mas uma boa prática.
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Adiciona uma classe CSS 'form-control' para estilização
            field.widget.attrs['class'] = 'form-control'