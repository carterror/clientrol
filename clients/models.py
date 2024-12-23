from django.db import models
from django.core.exceptions import ValidationError

def non_empty_field_warning(value): 
    raise ValidationError('Este campo no está lleno, pero no es obligatorio.')


# Create your models here.
class Client(models.Model):
    name = models.CharField('Nombres y apellido', max_length=100)
    phone = models.IntegerField('Teléfono', unique=True)
    email = models.EmailField('Correo electrónico', null=True, unique=True)

    address = models.TextField('Dirección')
    refer = models.CharField('Referido por', max_length=100, blank=True, null=True)

    created_at = models.DateTimeField('Creado', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizado', auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['name']
    
class Phone(models.Model):
    name = models.CharField('Detalle', max_length=100)
    number = models.CharField('Número', max_length=20, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='phones', verbose_name='Cliente')

    def __str__(self):
        return f'{self.client.name} {self.number}'
    
    class Meta:
        verbose_name = 'Teléfono'
        verbose_name_plural = 'Teléfonos'
        ordering = ['client']
