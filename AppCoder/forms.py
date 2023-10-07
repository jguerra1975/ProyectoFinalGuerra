from typing import Any
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from .models import *



class FormularioClientes(forms.ModelForm):
    class Meta:
        model=Clientes
        fields = ("dni", "nombre", "apellidoPaterno", "apellidoMaterno", "email")
        labels = {"dni": "DNI",
                  "nombre":"Nombre",
                  "apellidoPaterno": "Apellido Materno",
                  "apellidoMaterno": "Apellido Paterno",
                  "email": "Email"
                  }
        
class FormularioUsuarios(forms.ModelForm):
    class Meta:
        model=Usuarios
        fields = ("dni", "nombre", "apellidoPaterno", "apellidoMaterno", "email")
        labels = {"dni": "DNI",
                  "nombre":"Nombre",
                  "apellidoPaterno": "Apellido Materno",
                  "apellidoMaterno": "Apellido Paterno",
                  "email": "Email"
                  }
class UserCreateForm(UserCreationForm):

    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)

    class Meta:
        model=User
        fields = ("username", "password1", "password2")
        labels = {"username": "Nombre de Usuario"}

    def clean_password2(self):

        print(self.cleaned_data)

        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden!!!!")
        return password2

class UserEditForm(UserChangeForm):

    password = forms.CharField(
        help_text="",
        widget=forms.HiddenInput(), required=False
    )

    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)

    class Meta:
        model=User
        fields = ("password1", "password2")

    def clean_password2(self):

        print(self.cleaned_data)

        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden!!!!")
        return password2
class FormularioCategorias(forms.ModelForm):
    class Meta:
        
        model=Categorias
        fields = ("nombreCategoria", "ubicacion")
        labels = {"nombreCategoria": "Nombre Categoria",
                  "ubicacion":"Ubicacion",
                  }
        
class FormularioArticulos(forms.ModelForm):
    class Meta:
        
        model=Articulos
        fields = ("sku", "nombre", "precio", "id_categoria", "imagen")
        labels = {"sku": "SKU", "nombre": "Nombre", "precio": "Precio", "id_categoria": "Categoria", "imagen": "Imagen"}