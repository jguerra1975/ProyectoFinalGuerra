from django import forms

class FormularioClientes(forms.Form):
    dni = forms.CharField(max_length=9)
    nombre = forms.CharField(max_length=40)
    apellidoPaterno = forms.CharField(max_length=40)
    apellidoMaterno = forms.CharField(max_length=40)
    email = forms.EmailField()

class FormularioCategorias(forms.Form):
    nombreCategoria = forms.CharField(max_length=40)
    ubicacion = forms.CharField(max_length=40)

class FormularioArticulos(forms.Form):
    sku = forms.CharField(max_length=10)
    nombre = forms.CharField(max_length=40)
    precio = forms.IntegerField()