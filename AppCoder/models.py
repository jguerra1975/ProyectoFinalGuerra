from django.db import models

# Create your models here.

class Clientes(models.Model):
    dni = models.CharField(max_length=9)
    nombre = models.CharField(max_length=40)
    apellidoPaterno = models.CharField(max_length=40)
    apellidoMaterno = models.CharField(max_length=40)
    email = models.EmailField()

    def __str__(self):
        return f'{self.dni}  {self.nombre}  {self.apellidoPaterno} {self.apellidoMaterno} {self.email}'

class Categorias(models.Model):
    nombreCategoria = models.CharField(max_length=40)
    ubicacion = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return f'{self.nombreCategoria}  {self.ubicacion}'

class Articulos(models.Model):
    sku = models.CharField(max_length=10)
    nombre = models.CharField(max_length=40)
    precio = models.IntegerField()

    def __str__(self):
        return f'{self.sku}  {self.nombre}  {self.precio}'