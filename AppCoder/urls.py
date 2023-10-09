from django.urls import path
from django.contrib.auth.views import LogoutView
from AppCoder.views import *

urlpatterns = [
    path('', inicio, name="Inicio"),
    path('cliente/', Pagina_Cliente, name="Cliente"),
    path('crea-cliente/', Crea_Cliente, name="CreaCliente"),
    path('dato_creado/', Lista_Cliente, name="ListaCliente"),
    path('buscar-cliente/', Pagina_Cliente, name="BuscarCliente"),
    path('muestra-cliente/', Busca_Cliente, name="MuestraCliente"),
    path('cliente-list/', Cliente_List, name="ListarClientes"),
    path('DetalleClientes/<pk>/', ClienteDetail.as_view(), name="DetalleClientes"),
    path('EditarClientes/<int:id>/', ClienteUpdate, name="EditarClientes"),
    path('EliminarClientes/<int:id>/', ClienteDelete, name="EliminarClientes"),
    path('usuario/', Pagina_Usuario, name="Usuario"),
    path('crea-usuario/', Crea_Usuario, name="CreaUsuario"),
    path('dato_creado/', Lista_Usuario, name="ListaUsuario"),
    path('buscar-usuario/', Pagina_Usuario, name="BuscarUsuario"),
    path('muestra-usuario/', Busca_Usuario, name="MuestraUsuario"),
    path('usuario-list/', Usuario_List, name="ListarUsuarios"),
    path('DetalleUsuarios/<pk>/', UsuarioDetail.as_view(), name="DetalleUsuarios"),
    path('EditarUsuarios/<int:id>/', UsuarioUpdate, name="EditarUsuarios"),
    path('EliminarUsuarios/<int:id>/', UsuarioDelete, name="EliminarUsuarios"),
    path('categoria/', Pagina_Categoria, name="Categoria"),
    path('crea-categoria/', Crea_Categoria, name="CreaCategoria"),
    path('buscar-categoria/', Pagina_Categoria, name="BuscarCategoria"),
    path('categoria-list/', Categoria_List, name="ListarCategorias"),
    path('EliminarCategorias/<int:id>/', CategoriaDelete, name="EliminarCategorias"),
    path('EditarCategorias/<int:id>/', CategoriaUpdate, name="EditarCategorias"),
    path('DetalleCategorias/<pk>/', CategoriaDetail.as_view(), name="DetalleCategorias"),
    path('muestra-categoria/', Busca_Categoria, name="MuestraCategoria"),
    path('articulo/', Pagina_Articulo, name="Articulo"),
    path('crea-articulo/', Crea_Articulo, name="CreaArticulo"),
    path('buscar-articulo/', Pagina_Articulo, name="BuscarArticulo"),
    path('articulo-list/', Articulo_List, name="ListarArticulos"),
    path('EliminarArticulos/<int:id>/', ArticuloDelete, name="EliminarArticulos"),
    path('EditarArticulos/<int:id>/', ArticuloUpdate, name="EditarArticulos"),
    path('DetalleArticulos/<int:id>/', ArticuloDetail, name="DetalleArticulos"),
    path('muestra-articulo/', Busca_Articulo, name="MuestraArticulo"),
    path('comentario-articulo/<int:id>/', Comentario_Articulo_List, name="ComentarioArticulo"),
    path('crea-comentario/<int:id>/', CreaComentario, name="CrearComentario"),
    path('login/', loginView, name="Login"),
    path('logout/', LogoutView.as_view(template_name="logout.html"), name="Logout"),
    path('update_pass/', PasswordUpdate, name="CambiaPassword"),
    path('agregar-avatar/', agregar_avatar, name="AgregarAvatar"),
    path('contactanos/', contacto, name="mensajecontacto"),
    path('about/', mi_about, name="About"),
]