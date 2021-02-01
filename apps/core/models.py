from django.db import models

class Pessoa(models.Model):
    nome = models.CharField(max_length=120, blank=True)
    data_nasc = models.CharField(max_length=10, blank=True)

