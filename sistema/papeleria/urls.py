from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'papeleria'
urlpatterns = [
   path('index_pap/', views.index_pap, name='index_pap'),
   path('login/papeleria/', views.login_papeleria, name='login_papeleria'),
   path('logout_view/', views.logout_view, name='logout_view'),
   path("crear_articulo/", views.crear_articulo, name="crear_articulo"),
   path("editar_articulo/<int:articulo_id>/", views.editar_articulo, name="editar_articulo"),
   path("listar_articulo/", views.listar_articulo,name="listar_articulo"),
    path('buscar_articulo/', views.buscar_articulo, name='buscar_articulo'),
    path('eliminar_articulo/<int:id>', views.eliminar_articulo, name='eliminar_articulo'),
    path('verificar-nombre-articulo/', views.verificar_nombre_articulo, name='verificar_nombre_articulo'),
    path('validar_datos/', views.validar_datos, name='validar_datos'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
