from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
app_name = 'cafeteria'
urlpatterns = [
    path('', views.inicio, name='inicio'),
     path('login/cafeteria/', views.login_papeleria, name='login_cafeteria'),
    path('logout_caf/', views.logout_view, name='logout_caf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
