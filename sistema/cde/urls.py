from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
app_name = 'cde'
urlpatterns = [
    path('index_cde/', views.index_cde, name='index_cde'),
    path('login_cde/', views.login_cde, name='login_cde'),
    path('logout_cde/', views.logout_cde, name='logout_cde'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
