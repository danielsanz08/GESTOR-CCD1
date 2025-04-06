from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from .forms import LoginForm 
def index_caf(request):
    return render(request, 'index_caf/index_caf.html')
# Create your views here.
def login_cafeteria(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.module == 'Cafeteria':  # Verifica que el usuario pertenece a Cafetería
                    login(request, user)
                    messages.success(request, "Sesión iniciada correctamente en Cafetería.")
                    return redirect('index_caf')  # Redirige a la página de inicio de Cafetería
                else:
                    messages.error(request, "No tienes acceso a este módulo.")
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'login_caf/login_caf.html', {'form': form})


# CERRAR SESIÓN
def logout_caf(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect(reverse('libreria:inicio'))
User = get_user_model()