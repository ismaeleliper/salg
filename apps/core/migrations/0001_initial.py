# Generated by Django 3.1.2 on 2020-12-07 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=120)),
                ('data_nasc', models.CharField(blank=True, max_length=10)),
            ],
        ),
    ]
