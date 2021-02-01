from django import forms

from .models import Contribuinte


class ContribuinteForm(forms.ModelForm):
    class Meta:
        model = Contribuinte
        fields = ('nome', 'data_nasc', 'classe', 'contato')
        widgets = {
            'nome': forms.TextInput(attrs={
                'id': 'inputnome',
                'class': 'form-control',
                'placeholder': 'Nome Completo...'
            }),
            'data_nasc': forms.TextInput(attrs={'id': 'date',
                                                'class': 'form-control',
                                                'placeholder': 'ex: 01.01.1999'
                                                }),
            'classe': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'ex: Membro, Congregado ou Pastor...'}),
            'contato': forms.TextInput(attrs={'class': 'form-control', 'id': 'celular',
                                              'placeholder': 'ex: 47 99999-9999'})

        }
        exclude = ('user', )


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ContribuinteForm, self).__init__(*args, **kwargs)