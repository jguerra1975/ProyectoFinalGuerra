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
from .forms import FormularioClientes, FormularioCategorias, FormularioArticulos, UserCreateForm

# Create your views here.

def inicio(req):
    return render(req, "inicio.html")

########### Clientes ##############

def Pagina_Cliente(req):
    return render(req, "busca_cliente.html")

def Crea_Cliente(req):

    if req.method == 'POST':

        info = req.POST
        miFormulario = FormularioClientes({
            "dni": info["dni"],
            "nombre": info["nombre"].capitalize(),
            "apellidoPaterno": info["apellidoPaterno"].capitalize(),
            "apellidoMaterno": info["apellidoMaterno"].capitalize(),
            "email": info["email"]
        })
        userForm = UserCreateForm({
            "username": info["username"],
            "password1": info["password1"],
            "password2": info["password2"]
        })
        if miFormulario.is_valid() and userForm.is_valid():

            data = miFormulario.cleaned_data
            data.update(userForm.cleaned_data)
            user = User(username=data["username"], first_name=data["nombre"], last_name=data["apellidoPaterno"], email=data["email"])
            user.set_password(data["password1"])
            user.is_staff = True
            user.save()
            grupo = Group.objects.get(name='GrupoClientes')
            user.groups.add(grupo)
            
            cliente = Clientes(dni=data["dni"], nombre=data["nombre"], apellidoPaterno=data["apellidoPaterno"], apellidoMaterno=data["apellidoMaterno"], email=data["email"], user=user)
            cliente.save() 

            return render(req, "dato_creado.html", {"vista": 'Cliente'})
        else:
            return render(req, "FormularioClientes.html", {"miFormulario": miFormulario, "userForm": userForm})
    else:

        miFormulario = FormularioClientes()
        userForm = UserCreateForm()
        return render(req, "FormularioClientes.html", {"miFormulario": miFormulario, "userForm": userForm})
    

def Cliente_List(req):
    datos = Clientes.objects.all()
    print('method', req.method)
    print('GET', req.GET)
    print(f'{datos}')
    return render(req, "clientes_list.html", {"lista_clientes": datos})
        
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

class ClienteDetail(DetailView):
    model = Clientes
    template_name = "cliente_detail.html"
    context_object_name = "cliente"

def ClienteUpdate(req, id):
    cliente = Clientes.objects.get(id=id)
    print(f'{cliente.user}')
    if req.method == 'POST':

        miFormulario = FormularioClientes(req.POST)

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data
            cliente.dni = data["dni"]
            cliente.nombre = data["nombre"]
            cliente.apellidoPaterno = data["apellidoPaterno"]
            cliente.apellidoMaterno = data["apellidoMaterno"]
            cliente.email = data["email"]
            cliente.save()

            usuario = User.objects.get(username = cliente.user)
            usuario.first_name = data["nombre"]
            usuario.last_name = data["apellidoPaterno"]
            usuario.email = data["email"]
            usuario.save()

            datos = Clientes.objects.all()
            return render(req, "clientes_list.html", {"lista_clientes": datos})
    else:
        miFormulario = FormularioClientes({
            "dni": cliente.dni,
            "nombre": cliente.nombre.capitalize(),
            "apellidoPaterno": cliente.apellidoPaterno.capitalize(),
            "apellidoMaterno": cliente.apellidoMaterno.capitalize(),
            "email": cliente.email
            })
        return render(req, "cliente_update.html", {"miFormulario": miFormulario, "cliente": cliente})

def ClienteDelete(req, id):
    print('method', req.method)
    print('GET', req.GET)
    cliente = Clientes.objects.get(id=id)
    print (f'{cliente.user}')
    if req.method == 'POST':
        cliente.delete()
        usuario = User.objects.get(username = cliente.user)
        usuario.delete()
        cliente = Clientes.objects.all()
        return render(req, "clientes_list.html", {"lista_clientes": cliente})
    return render(req, "cliente_delete.html", {"cliente": cliente})



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
    
