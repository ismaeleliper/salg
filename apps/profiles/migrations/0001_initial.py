# Generated by Django 3.1.2 on 2020-12-09 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('pessoa_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.pessoa')),
                ('profile_image', models.ImageField(default='avatars/teste2.png', upload_to='avatars')),
                ('personal_contact', models.CharField(blank=True, max_length=120)),
                ('data_created', models.DateField(auto_now=True)),
                ('nome_da_igreja', models.CharField(blank=True, max_length=120)),
                ('cep', models.CharField(blank=True, max_length=10)),
                ('rua', models.CharField(blank=True, max_length=120)),
                ('numero', models.CharField(blank=True, max_length=120)),
                ('bairro', models.CharField(blank=True, max_length=120)),
                ('municipio', models.CharField(blank=True, max_length=120)),
                ('estado', models.CharField(blank=True, max_length=120)),
                ('telefone_fixo', models.CharField(blank=True, max_length=120)),
                ('movel', models.CharField(blank=True, max_length=120)),
                ('email_contato', models.EmailField(blank=True, max_length=120)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('core.pessoa',),
        ),
    ]