from django import forms
from .models import (
    Caixa, CreditoNoCaixa, DebitoNoCaixa,
    Oferta, LancamentoOferta
)

from bootstrap_modal_forms.forms import BSModalModelForm

from apps.contribuintes.models import Contribuinte


# ============= Formulário Caixas ===========================================


class CaixaForm(forms.ModelForm):
    class Meta:
        model = Caixa
        fields = ('nome', 'saldo', 'responsavel', 'descricao')
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'ex: Missionário, Alçadas, Construção...'}),
            'saldo': forms.TextInput(attrs={'class': 'form-control'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: Pastor Fulano...'}),
            'descricao': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class': 'form-control'})
        }

    def save(self, **kwargs):
        user = kwargs.pop('user')
        instance = super(CaixaForm, self).save(**kwargs)
        instance.user = user
        instance.save()
        return instance


class CreditoNoCaixaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CreditoNoCaixaForm, self).__init__(*args, **kwargs)
        self.fields['caixa'].queryset = Caixa.objects.filter(user=user)
        self.fields['cxa_a_debitar'].queryset = Caixa.objects.filter(user=user)

    class Meta:
        model = CreditoNoCaixa
        fields = ('caixa', 'cxa_a_debitar', 'valor', 'responsavel', 'info_adicional')
        widgets = {
            'caixa': forms.Select(attrs={'class': 'form-control'}),
            'cxa_a_debitar': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.TextInput(attrs={'class': 'form-control', 'id': 'inputValor'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: Pastor Fulano...'}),
            'info_adicional': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class': 'form-control'})
        }

    def save(self, **kwargs):
        user = kwargs.pop('user')
        instance = super(CreditoNoCaixaForm, self).save(**kwargs)
        instance.user = user
        instance.save()
        return instance


class DebitoNoCaixaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(DebitoNoCaixaForm, self).__init__(*args, **kwargs)
        self.fields['caixa'].queryset = Caixa.objects.filter(user=user)

    class Meta:
        model = DebitoNoCaixa
        fields = ('caixa', 'valor', 'congregacao', 'responsavel', 'info_adicional')

    def save(self, **kwargs):
        user = kwargs.pop('user')
        instance = super(DebitoNoCaixaForm, self).save(**kwargs)
        instance.user = user
        instance.save()
        return instance


# Ofertas Form
# ======================================================================================================

class OfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ('nome', 'tipo', 'responsavel', 'descricao')
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: Missionária, Construção...'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: Pastor Fulano...'}),
            'descricao': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class': 'form-control'})
        }

    def save(self, **kwargs):
        user = kwargs.pop('user')
        instance = super(OfertaForm, self).save(**kwargs)
        instance.user = user
        instance.save()
        return instance


class LancamentoOfertaForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(LancamentoOfertaForm, self).__init__(*args, **kwargs)
        self.fields['oferta'].queryset = Oferta.objects.filter(user=user)
        self.fields['contribuinte'].queryset = Contribuinte.objects.filter(user=user)
        self.fields['lancar_no_caixa'].queryset = Caixa.objects.filter(user=user)

    class Meta:
        model = LancamentoOferta
        fields = ('oferta', 'contribuinte', 'valor', 'lancar_no_caixa', 'info_adicional')
        widgets = {
            'oferta': forms.Select(attrs={'id': 'inputState', 'class': 'form-control'}),
            'valor': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Valor'}),
            'contribuinte': forms.Select(attrs={'class': 'form-control js-example-basic-single',
                                                'placeholder': 'Contribuinte',
                                                'id': 'inputContribuintes'}),
            'lancar_no_caixa': forms.Select(attrs={'class': 'form-control'}),
            'info_adicional': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class': 'form-control',
                                                    'id': 'selector'}),
        }

    def save(self, **kwargs):
        user = kwargs.pop('user')
        instance = super(LancamentoOfertaForm, self).save(**kwargs)
        instance.user = user
        instance.save()
        return instance


class FilterLancOfertas(forms.Form):
    ofertas = forms.ModelChoiceField(label="", queryset=None,
                                     widget=forms.Select(attrs={"class": "custom-select custom-select-sm",
                                                                "style": "max-width: 165px;"}),
                                     initial='Dizimos')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(FilterLancOfertas, self).__init__(*args, **kwargs)
        self.fields['ofertas'].queryset = Oferta.objects.filter(user=user)
