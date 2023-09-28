from django.urls import path
from AppCoder.views import inicio, Pagina_Cliente , Crea_Cliente, Lista_Cliente, Busca_Cliente, Pagina_Categoria, Crea_Categoria, Busca_Categoria, Pagina_Articulo, Crea_Articulo, Busca_Articulo

urlpatterns = [
    path('', inicio, name="Inicio"),
    path('cliente', Pagina_Cliente, name="Cliente"),
    path('crea-cliente', Crea_Cliente, name="CreaCliente"),
    path('dato_creado', Lista_Cliente, name="ListaCliente"),
    path('buscar-cliente', Busca_Cliente, name="BuscarCliente"),
    path('categoria', Pagina_Categoria, name="Categoria"),
    path('crea-categoria', Crea_Categoria, name="CreaCategoria"),
    path('buscar-categoria', Busca_Categoria, name="BuscarCategoria"),
    path('articulo', Pagina_Articulo, name="Articulo"),
    path('crea-articulo', Crea_Articulo, name="CreaArticulo"),
    path('buscar-articulo', Busca_Articulo, name="BuscarArticulo"),
]