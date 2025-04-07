from django.shortcuts import render
from papeleria.models import Articulo
from libreria.models import CustomUser
from papeleria.forms import LoginForm, ArticuloForm, ArticuloEditForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Create your views here.
def index_pap(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
    ]
    return render(request, 'index_pap/index_pap.html', {'breadcrumbs': breadcrumbs})
def login_papeleria(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.module == 'Papeleria':  # Verifica que el usuario pertenece a Papelería
                    login(request, user)
                    messages.success(request, "Sesión iniciada correctamente en Papelería.")
                    return redirect('papeleria:index_pap')  # Redirige a la página de inicio de Papelería
                else:
                    messages.error(request, "No tienes acceso a este módulo.")
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'login_pap/login_pap.html', {'form': form})

# CERRAR SESIÓN
def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect(reverse('libreria:inicio'))
User = get_user_model()


def crear_articulo(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        if form.is_valid():  # Corrección aquí
            articulo = form.save(commit=False)
            articulo.registrado_por = request.user
            articulo.save()
            return redirect('papeleria:listar_articulo')  # Redirección correcta
    else:
        form = ArticuloForm()
    
    return render(request, 'articulo/crear_articulo.html', {'form': form})
def editar_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    if request.method== 'POST':
        form = ArticuloEditForm(request.POST, instance=articulo)
        if form.is_valid():
            form.save()
            return redirect('papeleria:listar_articulo')
    else:
            form = ArticuloEditForm(instance=articulo)
    return render(request, 'articulo/editar_articulo.html', {'form': form, 'articulo': articulo})


def listar_articulo(request):
    query = request.GET.get('q', '').strip()
    articulos = Articulo.objects.select_related('registrado_por').all()


    if query:
        articulos = articulos.filter(
        Q(nombre__icontains=query) |
        Q(marca__icontains=query) |
        Q(observacion__icontains=query) |
        Q(tipo__icontains=query) |
        Q(precio__icontains=query) |
        Q(cantidad__icontains=query) |
        Q(registrado_por__username__icontains=query) |
        Q(fecha_registro__icontains=query)
    )

    paginator = Paginator(articulos, 5)
    page_number = request.GET.get('page')
    articulos = paginator.get_page(page_number)

    return render(request, 'articulo/listar_articulo.html', {'articulos': articulos})
def buscar_articulo(request):
    query = request.GET.get('q', '').strip()
    if query:
        articulos = Articulo.objects.filter(nombre__icontains=query).values(
            'id', 'nombre', 'marca', 'observacion', 'precio', 'registrado_por', 'fecha_registro'
        )
        return JsonResponse(list(articulos), safe=False)
    return JsonResponse([], safe=False)

def eliminar_articulo(request, id):
    articulo = Articulo.objects.get(id=id)
    if request.method == 'POST':
        articulo.delete()
        messages.success(request, "Artículo eliminado correctamente.")
        return redirect('papeleria:listar_articulo')
    return render(request, 'articulo/listar_articulo.html', {'articulo': articulo})

def validar_datos(request):
    email = request.GET.get('email', None)
    
    errores = {}

    # Validar correo electrónico
    if email and CustomUser.objects.filter(email=email).exists():
        errores['email'] = 'El email ya está en uso.'

    # Retornar los errores (si los hay) o una respuesta de validación exitosa
    return JsonResponse(errores if errores else {'valid': True})
def verificar_nombre_articulo(request):
    nombre = request.GET.get('nombre', '')
    existe = Articulo.objects.filter(nombre=nombre).exists()
    return JsonResponse({'existe': existe})
