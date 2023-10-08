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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.dni}  {self.nombre}  {self.apellidoPaterno} {self.apellidoMaterno} {self.email}'

class Categorias(models.Model):
    nombreCategoria = models.CharField(max_length=40,null=False,blank=False)
    ubicacion = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return f'{self.nombreCategoria}'

class Articulos(models.Model):
    sku = models.CharField(max_length=10,null=False,blank=False)
    nombre = models.CharField(max_length=40,null=False,blank=False)
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to='imagenes', null=True, blank=True)
    id_categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE,null=False,blank=False)

    def __str__(self):
        return f'{self.sku}  {self.nombre}  {self.precio}'

class ComentarioArticulos(models.Model):
    sku = models.ForeignKey(Articulos, on_delete=models.CASCADE,null=True, blank=True)
    comentario = models.CharField(max_length=255,null=False,blank=False)

    def __str__(self):
        return f'{self.sku}  {self.comentario}'

opciones_consulta = (
    [0, "Consulta"],
    [1, "Reclamo"],
    [2, "Sugerencia"],
    [3, "Felicitaciones"]
)

class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    tipo_consulta = models.IntegerField(choices=opciones_consulta)
    mensaje = models.TextField()
    avisos = models.BooleanField()

    def __str__(self):
        return self.nombre
    

class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='avatares', blank=True, null=True)

    def __str__(self):
        return f'{self.user}  {self.imagen}'