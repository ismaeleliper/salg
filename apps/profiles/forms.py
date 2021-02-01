from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('nome', 'data_nasc', 'profile_image', 'personal_contact',
                  'nome_da_igreja', 'cep', 'rua', 'numero', 'bairro', 'municipio', 'estado',
                  'telefone_fixo', 'movel', 'email_contato')
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Digite seu nome...',
                                           }),
            'data_nasc': forms.TextInput(attrs={'id': 'date',
                                                'class': 'form-control',
                                                'placeholder': 'ex: 01.01.1999',
                                                }),
            'profile_image': forms.FileInput(attrs={'id': 'imgInp', 'class': 'form-control', 'style': 'display: none'}),
            'personal_contact': forms.TextInput(attrs={'id': 'phone', 'class': 'form-control'}),

            'nome_da_igreja': forms.TextInput(attrs={'class': 'form-control', 'id': 'inputNomeIgreja'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'rua': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone_fixo': forms.TextInput(attrs={'class': 'form-control'}),
            'movel': forms.TextInput(attrs={'class': 'form-control'}),
            'email_contato': forms.EmailInput(attrs={'class': 'form-control'})

            # class="form-control" data-inputmask="'alias': 'dd/mm/yyyy'" data-mask
        }

# <input type="text" class="form-control" id="feNome" placeholder="First Name" value="Sierra">
