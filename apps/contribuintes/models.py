from django.db import models
from django.shortcuts import reverse

from apps.accounts.models import User
from apps.core.models import Pessoa


class Contribuinte(Pessoa):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contribuinte', blank=True, null=True)
    classe = models.CharField(max_length=120)
    contato = models.CharField(max_length=120, blank=True)
    fidelidade = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('contribuintes:detalhes_contribuinte', args=[self.id])
