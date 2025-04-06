from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
app_name = 'cafeteria'
urlpatterns = [
    path('', views.inicio, name='inicio'),
     path('login_cde/', views.login_papeleria, name='login_cde'),
    path('logout_cde/', views.logout_view, name='logout_cde'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
