from django.urls import path
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
    path('categoria/', Pagina_Categoria, name="Categoria"),
    path('crea-categoria/', Crea_Categoria, name="CreaCategoria"),
    path('buscar-categoria/', Busca_Categoria, name="BuscarCategoria"),
    path('articulo/', Pagina_Articulo, name="Articulo"),
    path('crea-articulo/', Crea_Articulo, name="CreaArticulo"),
    path('buscar-articulo/', Busca_Articulo, name="BuscarArticulo"),
]