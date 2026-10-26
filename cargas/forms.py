from django import forms

from .models import Carga


class CargaForm(forms.ModelForm):
    class Meta:
        model = Carga
        fields = [
            'codigo', 'descricao', 'cliente', 'origem', 'destino', 'tipo',
            'peso', 'valor', 'data_coleta', 'status', 'observacoes',
        ]
        widgets = {
            'data_coleta': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


