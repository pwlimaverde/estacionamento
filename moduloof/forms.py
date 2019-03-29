from django.forms import ModelForm
from .models import Orcamento_adesivo, Orcamento_filme

class OcadesivoForm(ModelForm):
    class Meta:
        model = Orcamento_adesivo
        fields = ['data', 'cliente', 'servico', 'material', 'acabamento', 'comp', 'larg', 'quantidade']


class OcfilmeForm(ModelForm):
    class Meta:
        model = Orcamento_filme
        fields = ['data', 'cliente', 'servico', 'material', 'acabamento', 'comp', 'larg', 'quantidade']
