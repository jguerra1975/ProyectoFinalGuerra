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
from .models import Articulos, Categorias, Clientes, Usuarios
from .forms import FormularioClientes, FormularioCategorias, FormularioArticulos, UserCreateForm, FormularioUsuarios, UserEditForm

# Create your views here.

def inicio(req):
    return render(req, "inicio.html")

########### Clientes ##############

def Pagina_Cliente(req):
    return render(req, "busca_cliente.html")

@login_required
def Crea_Cliente(req):
    groups_required = ['grupo1','grupos2']
    print(req.user.user_permissions.all())
    print(req.user.groups.all())
    grupos_usuario = req.user.groups.all().values('name')
    print (grupos_usuario)
    for grupo in grupos_usuario:
        print({grupo.values()})
        if grupo['name'] in groups_required:
            print ('esta dentro del grupo')
        else:
            print ('no esta en el grupo')

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
    
@login_required
def Cliente_List(req):
    datos = Clientes.objects.all()
    print('method', req.method)
    print('GET', req.GET)
    print(f'{datos}')
    return render(req, "clientes_list.html", {"lista_clientes": datos})

@login_required        
def Lista_Cliente(req):
    return render(req, "dato_creado.html")

@login_required
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

class ClienteDetail(LoginRequiredMixin, DetailView):
    model = Clientes
    template_name = "cliente_detail.html"
    context_object_name = "cliente"

@login_required
def ClienteUpdate(req, id):
    cliente = Clientes.objects.get(id=id)
    print(f'{cliente.user}')
    if req.method == 'POST':

        miFormulario = FormularioClientes(req.POST)

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data
            cliente.dni = data["dni"]
            cliente.nombre = data["nombre"].capitalize()
            cliente.apellidoPaterno = data["apellidoPaterno"].capitalize()
            cliente.apellidoMaterno = data["apellidoMaterno"].capitalize()
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

@login_required
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

########### Usuarios ##############
@login_required
def Pagina_Usuario(req):
    return render(req, "busca_usuarios.html")

@login_required
def Crea_Usuario(req):

    if req.method == 'POST':

        info = req.POST
        miFormulario = FormularioUsuarios({
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
            grupo = Group.objects.get(name='GrupoUsuarios')
            user.groups.add(grupo)
            print(f'{user}')
            usuario = Usuarios(dni=data["dni"], nombre=data["nombre"], apellidoPaterno=data["apellidoPaterno"], apellidoMaterno=data["apellidoMaterno"], email=data["email"], user=user)
            usuario.save() 

            return render(req, "dato_creado.html", {"vista": 'Usuario'})
        else:
            return render(req, "FormularioUsuarios.html", {"miFormulario": miFormulario, "userForm": userForm})
    else:

        miFormulario = FormularioUsuarios()
        userForm = UserCreateForm()
        return render(req, "FormularioUsuarios.html", {"miFormulario": miFormulario, "userForm": userForm})
    
@login_required
def Usuario_List(req):
    datos = Usuarios.objects.all()
    print('method', req.method)
    print('GET', req.GET)
    print(f'{datos}')
    return render(req, "usuarios_list.html", {"lista_usuarios": datos})

@login_required        
def Lista_Usuario(req):
    return render(req, "dato_creado.html")

@login_required
def Busca_Usuario(req: HttpRequest):
    print('method', req.method)
    print('GET', req.GET)
    if req.GET["nombre"]:
        dato = req.GET["nombre"]
        #datos = Clientes.objects.get(nombre=dato)
        #datos = Clientes.objects.filter(nombre=dato)
        datos = Usuarios.objects.filter(nombre__icontains=dato)
        print (f'{datos}')
        if datos.exists():
            pass
        else:
            datos = Usuarios.objects.filter(apellidoPaterno__icontains=dato)
            print ('paso el Apellido Paterno')
            if datos.exists():
               pass
            else:
                datos = Usuarios.objects.filter(apellidoMaterno__icontains=dato)
                print ('paso el Apellido Materno')
                if datos.exists():
                    pass
                else:
                    datos = Usuarios.objects.filter(dni__icontains=dato)
                    print ('paso el Apellido DNI')
                    if datos.exists():
                        pass
                    else:
                        return render(req, "no_existe_dato.html", {"vista": 'Usuarios'})

        return render(req, "Busqueda.html", {"datos": datos, "vista": "Usuarios"})
    else:
        return render(req, "no_existe_dato.html", {"vista": 'Usuarios'})


class UsuarioDetail(LoginRequiredMixin, DetailView):
    model = Usuarios
    template_name = "usuario_detail.html"
    context_object_name = "usuario"

@login_required
def UsuarioUpdate(req, id):
    usuario = Usuarios.objects.get(id=id)
    print(f'{usuario.user}')
    if req.method == 'POST':

        miFormulario = FormularioUsuarios(req.POST)

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data
            usuario.dni = data["dni"]
            usuario.nombre = data["nombre"].capitalize()
            usuario.apellidoPaterno = data["apellidoPaterno"].capitalize()
            usuario.apellidoMaterno = data["apellidoMaterno"].capitalize()
            usuario.email = data["email"]
            usuario.save()

            usuario_sistema = User.objects.get(username = usuario.user)
            usuario_sistema.first_name = data["nombre"]
            usuario_sistema.last_name = data["apellidoPaterno"]
            usuario_sistema.email = data["email"]
            usuario_sistema.save()

            datos = Usuarios.objects.all()
            return render(req, "usuarios_list.html", {"lista_usuarios": datos})
    else:
        miFormulario = FormularioUsuarios({
            "dni": usuario.dni,
            "nombre": usuario.nombre.capitalize(),
            "apellidoPaterno": usuario.apellidoPaterno.capitalize(),
            "apellidoMaterno": usuario.apellidoMaterno.capitalize(),
            "email": usuario.email
            })
        return render(req, "usuario_update.html", {"miFormulario": miFormulario, "usuario": usuario})

@login_required
def UsuarioDelete(req, id):
    print('method', req.method)
    print('GET', req.GET)
    usuario = Usuarios.objects.get(id=id)
    print (f'{usuario.user}')
    if req.method == 'POST':
        usuario.delete()
        usuario_sistema = User.objects.get(username = usuario.user)
        usuario_sistema.delete()
        usuario = Usuarios.objects.all()
        return render(req, "usuarios_list.html", {"lista_usuarios": usuario})
    return render(req, "usuario_delete.html", {"usuario": usuario})

########### Categorias ##############
@login_required
def Pagina_Categoria(req):
    return render(req, "categorias.html")

@login_required
def Crea_Categoria(req):
    print('method', req.method)
    print('POST', req.POST)
    if req.method == 'POST':
        miFormulario = FormularioCategorias(req.POST)
        if miFormulario.is_valid():
            data = miFormulario.cleaned_data
            categoria = Categorias(nombreCategoria=data["nombreCategoria"].upper(), 
                                   ubicacion=data["ubicacion"].upper()
                                   )
            categoria.save()
            return render(req, "dato_creado.html", {"vista": 'Categoria'})
    else:
        miFormulario = FormularioCategorias()
        return render(req, "FormularioCategorias.html", {"miFormulario": miFormulario})

@login_required
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

@login_required    
def Categoria_List(req):
    datos = Categorias.objects.all()
    print('method', req.method)
    print('GET', req.GET)
    print(f'{datos}')
    return render(req, "categorias_list.html", {"lista_categorias": datos})

@login_required
def CategoriaDelete(req, id):
    print('method', req.method)
    print('GET', req.GET)
    categoria = Categorias.objects.get(id=id)
    if req.method == 'POST':
        categoria.delete()
        categoria = Categorias.objects.all()
        return render(req, "categorias_list.html", {"lista_categorias": categoria})
    return render(req, "categoria_delete.html", {"categoria": categoria})

@login_required
def CategoriaUpdate(req, id):
    categoria = Categorias.objects.get(id=id)
    if req.method == 'POST':

        miFormulario = FormularioCategorias(req.POST)

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data
            categoria.nombreCategoria = data["nombreCategoria"].upper()
            categoria.ubicacion = data["ubicacion"].upper()
            categoria.save()
            datos = Categorias.objects.all()
            return render(req, "categorias_list.html", {"lista_categorias": datos})
    else:
        miFormulario = FormularioCategorias({
            "nombreCategoria": categoria.nombreCategoria.upper(),
            "ubicacion": categoria.ubicacion.upper()
            })
        return render(req, "categoria_update.html", {"miFormulario": miFormulario, "categoria": categoria})

class CategoriaDetail(LoginRequiredMixin, DetailView):
    model = Categorias
    template_name = "categoria_detail.html"
    context_object_name = "categoria"


########### Articulos ##############
@login_required
def Pagina_Articulo(req):
    return render(req, "articulos.html")

@login_required
def Crea_Articulo(req):
    print('method', req.method)
    print('POST', req.POST)
    if req.method == 'POST':
        miFormulario = FormularioArticulos(req.POST, req.FILES)
        if miFormulario.is_valid():
            data = miFormulario.cleaned_data
            articulo = Articulos(sku=data["sku"].upper(), 
                                   nombre=data["nombre"].upper(),
                                   precio=data["precio"],
                                   imagen=data["imagen"],
                                   id_categoria=data["id_categoria"]
                                )
            articulo.save()
            return render(req, "dato_creado.html", {"vista": 'articulo'})
    else:
        miFormulario = FormularioArticulos()
        return render(req, "FormularioArticulos.html", {"miFormulario": miFormulario})

@login_required
def Busca_Articulo(req: HttpRequest):
    print('method', req.method)
    print('GET', req.GET)
    if req.GET["nombre"]:
        dato = req.GET["nombre"]
        #datos = Categorias.objects.get(nombre=dato)
        #datos = Categorias.objects.filter(nombre=dato)
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

@login_required    
def Articulo_List(req):
    datos = Articulos.objects.all()
    print('method', req.method)
    print('GET', req.GET)
    print(f'{datos}')
    return render(req, "articulos_list.html", {"lista_articulos": datos})

@login_required
def ArticuloDelete(req, id):
    print('method', req.method)
    print('GET', req.GET)
    articulo = Articulos.objects.get(id=id)
    if req.method == 'POST':
        articulo.delete()
        articulo = Articulos.objects.all()
        return render(req, "articulos_list.html", {"lista_articulos": articulo})
    return render(req, "articulo_delete.html", {"articulo": articulo})

@login_required
def ArticuloUpdate(req, id):
    articulo = Articulos.objects.get(id=id)
    if req.method == 'POST':

        miFormulario = FormularioArticulos(req.POST, req.FILES)

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data
            articulo.sku = data["sku"]
            articulo.nombre = data["nombre"].upper()
            articulo.precio = data["precio"]
            articulo.id_categoria = data["id_categoria"]
            articulo.imagen = data["imagen"]
            articulo.save()
            datos = Articulos.objects.all()
            return render(req, "articulos_list.html", {"lista_articulos": datos})
    else:
        miFormulario = FormularioArticulos({
            "sku": articulo.sku,
            "nombre": articulo.nombre.upper(),
            "precio": articulo.precio,
            "id_categoria": articulo.id_categoria,
            "imagen": articulo.imagen
            })
        return render(req, "articulo_update.html", {"miFormulario": miFormulario, "articulo": articulo})

@login_required    
def ArticuloDetail(req, id):
    articulo = Articulos.objects.get(id=id)
    return render(req, "articulo_detail.html", {"articulo": articulo})

def loginView(req):

    if req.method == 'POST':

        miFormulario = AuthenticationForm(req, data=req.POST)

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data
            usuario = data["username"]
            psw = data["password"]
            nombre = User.objects.get(username = usuario)
            print(f'{nombre.first_name}')

            user = authenticate(username=usuario, password=psw)
            if user:
                login(req, user)
                print(f'{user.first_name}')
                return render(req, "inicio.html", {"mensaje": f"Bienvenido {nombre}!"})
            
        return render(req, "inicio.html", {"mensaje": f"Datos incorrectos"})
    else:
        miFormulario = AuthenticationForm()
        return render(req, "login.html", {"miFormulario": miFormulario})
   
def PasswordUpdate(req):

    usuario = req.user
    if req.method == 'POST':

        miFormulario = UserEditForm(req.POST, instance=req.user)

        if miFormulario.is_valid():
            
            data = miFormulario.cleaned_data
            usuario.set_password(data["password1"])
            usuario.save()

            return render(req, "mensajes.html", {"mensaje": "Datos actualizados con éxito!"})
        else:
            return render(req, "cambia_password.html", {"miFormulario": miFormulario})

    else:
        miFormulario = UserEditForm(instance=usuario)
        return render(req, "cambia_password.html", {"miFormulario": miFormulario})