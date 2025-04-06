from django.shortcuts import render
from libreria.models import CustomUser
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