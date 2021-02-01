from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import User
from apps.contribuintes.models import Contribuinte


# ============= Modelo Caixas ===========================================


class Caixa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='caixa')
    nome = models.CharField(max_length=120)
    saldo = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    responsavel = models.CharField(max_length=120)
    descricao = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nome

@receiver(post_save, sender=User)
def create_caixa_dizimo(sender, **kwargs):
    if kwargs.get('created', False):
        Caixa.objects.create(user=kwargs['instance'], nome="Dizimos", saldo=0.0, responsavel="Admin")



# ============= Modelo Movimentações entre Caixas ===========================================


# Registro de Entradas
class CreditoNoCaixa(models.Model):
    class Meta:
        ordering = ('-date_entrada', 'valor')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creditonocaixa')
    sigla = models.CharField(max_length=500, blank=True)
    caixa = models.ForeignKey(Caixa, on_delete=models.CASCADE)
    cxa_a_debitar = models.ForeignKey(Caixa, on_delete=models.CASCADE, related_name='cxdebitar')
    valor = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    date_entrada = models.DateField(auto_now_add=True)
    responsavel = models.CharField(max_length=120)
    info_adicional = models.TextField(max_length=120, blank=True, null=True)


# Registro de Saídas
class DebitoNoCaixa(models.Model):
    class Meta:
        ordering = ('-date_saida', 'valor')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='debitonocaixa')
    sigla = models.CharField(max_length=500, blank=True)
    caixa = models.ForeignKey(Caixa, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    date_saida = models.DateField(auto_now_add=True)
    congregacao = models.CharField(max_length=120)
    responsavel = models.CharField(max_length=120)
    info_adicional = models.TextField(max_length=120, blank=True, null=True)


# ============= Modelo Ofertas ===========================================


DIZIMO = '1'
ALCADA = '2'
MISSIONARIA = '3'
PERSONALIZADA = '4'
CHOICES = (
    (DIZIMO, 'Dízimo'),
    (ALCADA, 'Alçada'),
    (MISSIONARIA, 'Missionária'),
    (PERSONALIZADA, 'Personalizada')
)

class Oferta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='oferta')
    nome = models.CharField(max_length=120)
    tipo = models.CharField(max_length=1, choices=CHOICES, default=PERSONALIZADA)
    responsavel = models.CharField(max_length=120)
    descricao = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nome

@receiver(post_save, sender=User)
def create_dizimo(sender, **kwargs):
    if kwargs.get('created', False):
        Oferta.objects.create(user=kwargs['instance'], nome="Dizimos", tipo="1", responsavel="Administrador")


# ====================== Modelo Lançamentos =========================================


class LancamentoOferta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lancamentooferta')
    sigla = models.CharField(max_length=500, blank=True)
    oferta = models.ForeignKey(Oferta, on_delete=models.DO_NOTHING)
    valor = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    date = models.DateField(auto_now_add=True)
    contribuinte = models.ForeignKey(Contribuinte, on_delete=models.CASCADE, related_name='contribuinte')
    lancar_no_caixa = models.ForeignKey(Caixa, on_delete=models.DO_NOTHING)
    info_adicional = models.TextField(max_length=120, blank=True)


# ====================== Modelo Contas =========================================

#CONTA_OPERACAO_DEBITO = 'd'
#CONTA_OPERACAO_CREDITO = 'c'
#CONTA_OPERACAO_CHOICES = (
#    (CONTA_OPERACAO_DEBITO, 'Debito'),
#    (CONTA_OPERACAO_CREDITO, 'Credito'),
#)

#CONTA_STATUS_APAGAR = 'a'
#CONTA_STATUS_PAGO = 'p'
#CONTA_STATUS_CHOICES = (
#    (CONTA_STATUS_APAGAR, 'À Pagar'),
#    (CONTA_STATUS_PAGO, 'Pago'),
#)


#class Conta(models.Model):
#    class Meta:
#        ordering = ('-data_vencimento', 'valor')

#    referencia = models.CharField(max_length=500, blank=True)
#    fornecedor = models.CharField(max_length=120)
#    data_vencimento = models.DateField()
#    data_pagamento = models.DateField(null=True, blank=True)
#    valor = models.DecimalField(max_digits=20, decimal_places=2)
#    operacao = models.CharField(
#        max_length=1,
#        default=CONTA_OPERACAO_DEBITO,
#        choices=CONTA_OPERACAO_CHOICES,
#        blank=True,
#    )
#    status = models.CharField(
#        max_length=1,
#        default=CONTA_STATUS_APAGAR,
#        choices=CONTA_STATUS_CHOICES,
#        blank=True,
#    )
#    responsavel = models.CharField(max_length=120, blank=True)
#    descricao = models.TextField(blank=True)


#def incrementar_num_ref_conta_a_pagar():
#    ultimo_ = ContaPagar.objects.all().order_by('id').last()
#    if not ultimo_:
#        return 'CONTAPAGAR1'
#    else:
#        referencia = ultimo_.referencia
#        ref_int = int(referencia.split('CONTAPAGAR')[-1])
#        new_ref_int = ref_int + 1
#        new_referencia = 'CONTAPAGAR' + str(new_ref_int)
#        return new_referencia


#class ContaPagar(Conta):
#    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contapagar')
#
#    def save(self, *args, **kwargs):
#        self.referencia = incrementar_num_ref_conta_a_pagar()
#        self.operacao = CONTA_OPERACAO_DEBITO
#        super(ContaPagar, self).save(*args, **kwargs)


#def incrementar_num_ref_conta_a_receber():
#    ultimo_ = ContaPagar.objects.all().order_by('id').last()
#    if not ultimo_:
#        return 'ARECEBER1'
#    else:
#        referencia = ultimo_.referencia
#        ref_int = int(referencia.split('ARECEBER')[-1])
#        new_ref_int = ref_int + 1
#        new_referencia = 'ARECEBER' + str(new_ref_int)
#        return new_referencia


#class ContaReceber(Conta):
#    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contareceber')

#    def save(self, *args, **kwargs):
#        self.referencia = incrementar_num_ref_conta_a_receber()
#        self.operacao = CONTA_OPERACAO_CREDITO
#        super(ContaReceber, self).save(*args, **kwargs)
