from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User, Group
from .models import Articulos, Categorias, Clientes
from .forms import FormularioClientes, FormularioCategorias, FormularioArticulos

# Create your views here.

def inicio(req):
    return render(req, "inicio.html")

########### Clientes ##############

def Pagina_Cliente(req):
    return render(req, "clientes.html")

#def Crea_Cliente(req):
#    print('method', req.method)
#    print('POST', req.POST)
#    if req.method == 'POST':
#        miFormulario = FormularioClientes(req.POST)
#        if miFormulario.is_valid():
#            data = miFormulario.cleaned_data
#            cliente = Clientes(dni=data["dni"], nombre=data["nombre"], apellidoPaterno=data["apellidoPaterno"], apellidoMaterno=data["apellidoMaterno"], email=data["email"])
#            cliente.save()
#            return render(req, "dato_creado.html", {"vista": 'Cliente'})
#    else:
#        miFormulario = FormularioClientes()
#        return render(req, "FormularioClientes.html", {"miFormulario": miFormulario})
        
def Lista_Cliente(req):
    return render(req, "dato_creado.html")

def Busca_Cliente(req: HttpRequest):
    print('method', req.method)
    print('GET', req.GET)
    if req.GET["nombre"]:
        dato = req.GET["nombre"]
        #datos = Clientes.objects.get(nombre=dato)
        #datos = Clientes.objects.filter(nombre=dato)
        datos = Clientes.objects.filter(nombre__icontains=dato)
        print (f'{datos}')
        if datos.exists():
            pass
        else:
            datos = Clientes.objects.filter(apellidoPaterno__icontains=dato)
            print ('paso el Apellido Paterno')
            if datos.exists():
               pass
            else:
                datos = Clientes.objects.filter(apellidoMaterno__icontains=dato)
                if datos.exists():
                    pass
                else:
                    datos = Clientes.objects.filter(dni__icontains=dato)
                    if datos.exists():
                        pass
                    else:
                        return render(req, "no_existe_dato.html", {"vista": 'Clientes'})

        return render(req, "Busqueda.html", {"datos": datos, "vista": "Clientes"})
    else:
        return render(req, "no_existe_dato.html", {"vista": 'Clientes'})
    
########### Categorias ##############

def Pagina_Categoria(req):
    return render(req, "categorias.html")

def Crea_Categoria(req):
    print('method', req.method)
    print('POST', req.POST)
    if req.method == 'POST':
        miFormulario = FormularioCategorias(req.POST)
        if miFormulario.is_valid():
            data = miFormulario.cleaned_data
            categoria = Categorias(nombreCategoria=data["nombreCategoria"], ubicacion=data["ubicacion"])
            categoria.save()
            return render(req, "dato_creado.html", {"vista": 'Categoria'})
    else:
        miFormulario = FormularioCategorias()
        return render(req, "FormularioCategorias.html", {"miFormulario": miFormulario})

def Busca_Categoria(req: HttpRequest):
    print('method', req.method)
    print('GET', req.GET)
    if req.GET["nombre"]:
        dato = req.GET["nombre"]
        #datos = Categorias.objects.get(nombre=dato)
        #datos = Categorias.objects.filter(nombre=dato)
        datos = Categorias.objects.filter(nombreCategoria__icontains=dato)
        print (f'{datos}')
        if datos.exists():
            pass
        else:
            datos = Categorias.objects.filter(ubicacion__icontains=dato)
            if datos.exists():
                pass
            else:
                return render(req, "no_existe_dato.html", {"vista": 'Categorias'})

        return render(req, "Busqueda.html", {"datos": datos, "vista": "Categorias"})
    else:
        return render(req, "no_existe_dato.html", {"vista": 'Categorias'})
    
########### Articulos ##############

def Pagina_Articulo(req):
    return render(req, "articulos.html")

def Crea_Articulo(req):
    print('method', req.method)
    print('POST', req.POST)
    if req.method == 'POST':
        miFormulario = FormularioArticulos(req.POST)
        if miFormulario.is_valid():
            data = miFormulario.cleaned_data
            articulo = Articulos(sku=data["sku"], nombre=data["nombre"], precio=data["precio"])
            articulo.save()
            return render(req, "dato_creado.html", {"vista": 'Articulo'})
    else:
        miFormulario = FormularioArticulos()
        return render(req, "FormularioArticulos.html", {"miFormulario": miFormulario})

def Busca_Articulo(req: HttpRequest):
    print('method', req.method)
    print('GET', req.GET)
    if req.GET["nombre"]:
        dato = req.GET["nombre"]
        #datos = Articulos.objects.get(nombre=dato)
        #datos = Articulos.objects.filter(nombre=dato)
        datos = Articulos.objects.filter(sku__icontains=dato)
        print (f'{datos}')
        if datos.exists():
            pass
        else:
            datos = Articulos.objects.filter(nombre__icontains=dato)
            if datos.exists():
                pass
            else:
                return render(req, "no_existe_dato.html", {"vista": 'Articulos'})

        return render(req, "Busqueda.html", {"datos": datos, "vista": "Articulos"})
    else:
        return render(req, "no_existe_dato.html", {"vista": 'Articulos'})
    
def Crea_Cliente(req):

    if req.method == 'POST':

        info = req.POST

        miFormulario = FormularioClientes({
            "dni": info["dni"],
            "nombre": info["nombre"],
            "apellidoPaterno": info["apellidoPaterno"],
            "apellidoMaterno": info["apellidoMaterno"],
            "email": info["email"]
        })
        userForm = UserCreationForm({
            "username": info["username"],
            "password1": info["password1"],
            "password2": info["password2"]
        })
        if miFormulario.is_valid() and userForm.is_valid():

            data = miFormulario.cleaned_data
            data.update(userForm.cleaned_data)

            user = User(username=data["username"])
            user.set_password(data["password1"])
            user.save()

            grupo = Group.objects.get(name='GrupoClientes')
            user.groups.add(grupo)

            cliente = Clientes(dni=data["dni"], nombre=data["nombre"], apellidoPaterno=data["apellidoPaterno"], apellidoMaterno=data["apellidoMaterno"], email=data["email"], user=user)
            cliente.save() 

            return render(req, "dato_creado.html", {"vista": 'Cliente'})
    else:

        miFormulario = FormularioClientes()
        userForm = UserCreationForm()
        return render(req, "FormularioClientes.html", {"miFormulario": miFormulario, "userForm": userForm})