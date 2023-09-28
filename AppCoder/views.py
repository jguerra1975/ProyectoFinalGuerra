from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .models import Articulos, Categorias, Clientes
from .forms import FormularioClientes, FormularioCategorias, FormularioArticulos

# Create your views here.

def inicio(req):
    return render(req, "inicio.html")

########### Clientes ##############

def Pagina_Cliente(req):
    return render(req, "clientes.html")

def Crea_Cliente(req):
    print('method', req.method)
    print('POST', req.POST)
    if req.method == 'POST':
        miFormulario = FormularioClientes(req.POST)
        if miFormulario.is_valid():
            data = miFormulario.cleaned_data
            cliente = Clientes(dni=data["dni"], nombre=data["nombre"], apellidoPaterno=data["apellidoPaterno"], apellidoMaterno=data["apellidoMaterno"], email=data["email"])
            cliente.save()
            return render(req, "dato_creado.html", {"vista": 'Cliente'})
    else:
        miFormulario = FormularioClientes()
        return render(req, "FormularioClientes.html", {"miFormulario": miFormulario})
        
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