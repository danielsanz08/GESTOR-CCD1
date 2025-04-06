from django.shortcuts import render

# Create your views here.
def login_cde(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.module == 'Centro de eventos':  # Verifica que el usuario pertenece a CDE
                    login(request, user)
                    messages.success(request, "Sesión iniciada correctamente en CDE.")
                    return redirect('index_cde')  # Redirige a la página de inicio de CDE
                else:
                    messages.error(request, "No tienes acceso a este módulo.")
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'cde//login/login_cde.html', {'form': form})

def logout_caf(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect(reverse('libreria:inicio'))
User = get_user_model()

def index_cde(request):
    return render(request, 'index_cde/index_cde.html')