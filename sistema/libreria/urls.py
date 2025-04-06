from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
app_name = 'libreria'
urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
   
    #RESTABLECER CONTRASEÑA 
    path("reset_password/", views.password_reset_request, name="password_reset"),
    path("reset_password/done/", views.password_reset_done, name="password_reset_done"),
    path("reset_password/confirm/<uidb64>/<token>/", views.password_reset_confirm, name="password_reset_confirm"),
    path("reset_password/complete/", views.password_reset_complete, name="password_reset_complete"),
    path('validar_datos/', views.validar_datos, name='validar_datos'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
