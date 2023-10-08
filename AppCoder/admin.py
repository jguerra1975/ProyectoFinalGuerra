from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Usuarios)
admin.site.register(Clientes)
admin.site.register(Categorias)
admin.site.register(Articulos)
admin.site.register(Avatar)
admin.site.register(ComentarioArticulos)
admin.site.register(Contacto)