from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'papeleria'
urlpatterns = [
   path('index_pap/', views.index_pap, name='index_pap'),
   path('login/papeleria/', views.login_papeleria, name='login_papeleria'),
   path('logout_view/', views.logout_view, name='logout_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
