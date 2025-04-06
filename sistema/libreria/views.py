from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login
from .forms import CustomUserForm, LoginForm
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import logout

# Create your views here.
# Página de inicio
def inicio(request):
    return render(request, 'index/index.html')

def crear_usuario(request):
    admin_exists = CustomUser.objects.exists()

    if request.method == 'POST':
        form = CustomUserForm(request.POST)

        if form.is_valid():
            try:
                user = form.save(commit=False)
                module = user.module
                role = user.role

                # Verificar el número de administradores en cada módulo
                if role == 'Administrador':
                    admin_count = CustomUser.objects.filter(
                        role='Administrador', module=module, is_active=True
                    ).count()

                    limits = {'Papeleria': 3, 'Cafeteria': 2, 'Centro de eventos': 1}
                    if module in limits and admin_count >= limits[module]:
                        messages.error(request, f"Ya existen {limits[module]} administradores en el módulo {module}.")
                        return redirect('crear_usuario')

                # Guardar el usuario
                user.save()

           
                # Enviar correo a los administradores del mismo módulo
                admin_emails = CustomUser.objects.filter(
                    role='Administrador', module=module, is_active=True
                ).values_list('email', flat=True)
                cargo = request.POST.get("cargo", "").strip()
                email = request.POST.get("email", "").strip()
                if admin_emails:
                    subject = f"Nuevo usuario creado en {module}"
                    message = f"Hola querido usuario,\n\nPor parte de Gestor CCD, te informamos que se ha creado un nuevo usuario. \n Información: Nombre: {user.username} \n Rol: {role} Módulo: {module}\n Cargo: {cargo}\n Email: {email}\n\nEn caso de ser infiltrado, por favor te invitamos a desactivarlo.\n\nMuchas gracias por su atención. El director de Gestor CCD te desea un feliz día."
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, list(admin_emails))

                messages.success(request, f"Usuario '{user.username}' creado exitosamente.")
                return redirect('libreria:inicio')

            except Exception as e:
                messages.error(request, f"Hubo un error al crear el usuario: {e}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    else:
        form = CustomUserForm()

    return render(request, 'usuario/crear_usuario.html', {'form': form, 'admin_exists': admin_exists})


def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(
                reverse("libreria:password_reset_confirm", kwargs={"uidb64": uid, "token": token})
            )

            # Enviar correo con el enlace de restablecimiento
            subject = "Restablecer tu contraseña"
            message = render_to_string("password_reset_email.html", {"reset_link": reset_link})
            send_mail(subject, message, "noreply@tuweb.com", [user.email])

            return redirect(reverse("libreria:password_reset_done") + "?sent=true")  # Indica que el correo fue enviado
        except User.DoesNotExist:
            return redirect(reverse("libreria:password_reset_done") + "?sent=false")  # Indica que el correo no existe

    return render(request, "password_reset.html")

def password_reset_done(request):
    return render(request, "password_reset_done.html")

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse("libreria:password_reset_complete"))
        else:
            form = SetPasswordForm(user)  # Asegura que el formulario se pase correctamente
        return render(request, "password_reset_confirm.html", {"form": form})
    else:
        return render(request, "password_reset_confirm.html", {"error": "El enlace no es válido o ha expirado."})

def password_reset_complete(request):
    return render(request, "password_reset_complete.html")

#VALIDAR INFORMACION
def validar_datos(request):
    email = request.GET.get('email', None)
    
    errores = {}

    # Validar correo electrónico
    if email and CustomUser.objects.filter(email=email).exists():
        errores['email'] = 'El email ya está en uso.'

    # Retornar los errores (si los hay) o una respuesta de validación exitosa
    return JsonResponse(errores if errores else {'valid': True})

