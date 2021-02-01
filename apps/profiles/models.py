from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import User
from apps.core.models import Pessoa


class Profile(Pessoa):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='profile')
    profile_image = models.ImageField(upload_to='avatars', default='avatars/teste3.png')
    personal_contact = models.CharField(max_length=120, blank=True)
    data_created = models.DateField(auto_now=True)

    nome_da_igreja = models.CharField(max_length=120, blank=True)
    cep = models.CharField(max_length=10, blank=True)
    rua = models.CharField(max_length=120, blank=True)
    numero = models.CharField(max_length=120, blank=True)
    bairro = models.CharField(max_length=120, blank=True)
    municipio = models.CharField(max_length=120, blank=True)
    estado = models.CharField(max_length=120, blank=True)
    telefone_fixo = models.CharField(max_length=120, blank=True)
    movel = models.CharField(max_length=120, blank=True)
    email_contato = models.EmailField(max_length=120, blank=True)


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.create(user=kwargs['instance'])