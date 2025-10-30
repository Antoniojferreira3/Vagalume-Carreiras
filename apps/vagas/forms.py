# Arquivo: apps/vagas/forms.py

from django import forms
from .models import Vaga

class VagaForm(forms.ModelForm):
    
    class Meta:
        model = Vaga
        # Define os campos que o recrutador irá preencher
        fields = [
            'titulo', 'descricao', 'requisitos', 'tipo_contrato', 
            'localidade', 'beneficios', 'faixa_salarial', 'status'
        ]
        
        # Define widgets para campos de texto maiores
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 5}),
            'requisitos': forms.Textarea(attrs={'rows': 5}),
            'beneficios': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        # A 'view' (que faremos depois) deve passar a 'empresa'
        self.empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)
        
        # (Semana 6): Adiciona classes de CSS (ex: Bootstrap/Tailwind)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control' # Exemplo

    def clean_titulo(self):
        """
        VALIDAÇÃO DE DADOS:
        Impede que a mesma empresa cadastre duas vagas com o mesmo título.
        """
        titulo = self.cleaned_data.get('titulo')
        
        if not self.empresa:
            # Isso não deve acontecer se a view for configurada corretamente
            raise forms.ValidationError("Erro interno: Empresa não identificada.")

        # Procura por vagas da MESMA empresa com o MESMO título
        # self.instance é a vaga sendo editada (se for o caso)
        query = Vaga.objects.filter(
            empresa=self.empresa, 
            titulo__iexact=titulo # ignora maiúscula/minúscula
        )
        
        # Se estiver editando, exclui a própria vaga da checagem
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        
        if query.exists():
            raise forms.ValidationError("Sua empresa já possui uma vaga cadastrada com este título.")
            
        return titulo

    def save(self, commit=True, recrutador=None):
        """
        Sobrescreve o 'save' para popular os campos 'empresa' e 'recrutador'
        automaticamente com base no usuário logado (passado pela view).
        """
        vaga = super().save(commit=False)
        
        if recrutador:
            vaga.recrutador = recrutador
            vaga.empresa = recrutador.empresa # Pega a empresa do recrutador
        elif self.empresa: # Fallback caso a empresa seja passada
             vaga.empresa = self.empresa
            
        if commit:
            vaga.save()
            
        return vaga
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