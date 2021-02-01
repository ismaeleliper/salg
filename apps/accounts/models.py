from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        'username',
        max_length=50,
        unique=True,
        help_text='Requerido. 50 caracteres ou menos. Letras, dígitos e @ /. / + / - / _ apenas.',
        error_messages={
            'unique': "Um usuário com esse username já existe.",
        },
    )
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'admin', ]

    def get_absolute_url(self):
        return reverse('profiles:config', args=[self.id])

    def __unicode__(self):
        return self.email
