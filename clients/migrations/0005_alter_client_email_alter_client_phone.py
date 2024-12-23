# Generated by Django 5.1.4 on 2024-12-11 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_client_email_alter_client_refer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True, verbose_name='Correo electrónico'),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.IntegerField(unique=True, verbose_name='Teléfono'),
        ),
    ]