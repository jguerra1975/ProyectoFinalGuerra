from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import *

class FormularioCategorias(forms.Form):
    nombreCategoria = forms.CharField(max_length=40)
    ubicacion = forms.CharField(max_length=40)

class FormularioArticulos(forms.Form):
    sku = forms.CharField(max_length=10)
    nombre = forms.CharField(max_length=40)
    precio = forms.IntegerField()

class FormularioClientes(forms.ModelForm):

    class Meta:
        model=Clientes
        fields = ("dni", "nombre", "apellidoPaterno", "apellidoMaterno", "email")

