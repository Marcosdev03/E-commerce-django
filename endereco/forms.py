from django import forms

from .models import Endereco


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = [
            'cep',
            'rua',
            'numero',
            'complemento',
            'bairro',
            'cidade',
            'estado',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_cep(self):
        cep = ''.join(filter(str.isdigit, self.cleaned_data.get('cep', '')))
        if len(cep) != 8:
            raise forms.ValidationError('Digite um CEP válido com 8 dígitos.')
        return cep
