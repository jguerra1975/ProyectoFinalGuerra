from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.
class Clientes(models.Model):
    dni = models.CharField(max_length=9,null=False,blank=False)
    nombre = models.CharField(max_length=40,null=False,blank=False)
    apellidoPaterno = models.CharField(max_length=40)
    apellidoMaterno = models.CharField(max_length=40)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #grupo = models.OneToOneField(Group, on_delete=models.CASCADE,null=True ,blank=True)


    def __str__(self):
        return f'{self.dni}  {self.nombre}  {self.apellidoPaterno} {self.apellidoMaterno} {self.email}'
    
class Usuarios(models.Model):
    dni = models.CharField(max_length=9,null=False,blank=False)
    nombre = models.CharField(max_length=40,null=False,blank=False)
    apellidoPaterno = models.CharField(max_length=40)
    apellidoMaterno = models.CharField(max_length=40)
    email = models.EmailField()

    def __str__(self):
        return f'{self.dni}  {self.nombre}  {self.apellidoPaterno} {self.apellidoMaterno} {self.email}'

class Categorias(models.Model):
    nombreCategoria = models.CharField(max_length=40,null=False,blank=False)
    ubicacion = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return f'{self.nombreCategoria}  {self.ubicacion}'

class Articulos(models.Model):
    sku = models.CharField(max_length=10,null=False,blank=False)
    nombre = models.CharField(max_length=40,null=False,blank=False)
    precio = models.IntegerField()
    id_categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE,null=False,blank=False)

    def __str__(self):
        return f'{self.sku}  {self.nombre}  {self.precio}'