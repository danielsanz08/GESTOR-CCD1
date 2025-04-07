from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'libreria'

urlpatterns = [
    path('papeleria/', include(('papeleria.urls', 'papeleria'), namespace='papeleria')),
    path('cafeteria/', include(('cafeteria.urls', 'cafeteria'), namespace='cafeteria')),
    path('cde/', include(('cde.urls', 'cde'), namespace='cde')),

    path('', views.inicio, name='inicio'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('ver_usuario/<int:user_id>/', views.ver_usuario, name='ver_usuario'),
    path('editar_usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('lista_usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('cambiar-estado-usuario/<int:user_id>/', views.cambiar_estado_usuario, name='cambiar_estado_usuario'),
    # RESTABLECER CONTRASEÑA 
    path("reset_password/", views.password_reset_request, name="password_reset"),
    path("reset_password/done/", views.password_reset_done, name="password_reset_done"),
    path("reset_password/confirm/<uidb64>/<token>/", views.password_reset_confirm, name="password_reset_confirm"),
    path("reset_password/complete/", views.password_reset_complete, name="password_reset_complete"),

    path('validar_datos/', views.validar_datos, name='validar_datos'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
