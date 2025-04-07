from django import forms
from .models import CustomUser
class CustomUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        required=True
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'cargo', 'module', 'password']

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        
        # Agregar clases CSS a los campos
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Correo electrónico'})
        self.fields['role'].widget.attrs.update({'class': 'form-select'})
        self.fields['cargo'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Cargo'})
        self.fields['module'].widget.attrs.update({'class': 'form-select'})

        # Si el usuario ya existe, deshabilitar el campo 'module' (no puede cambiar su módulo)
        if self.instance.pk:
            self.fields['module'].widget.attrs['disabled'] = True

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("La contraseña es obligatoria.")
        return password

    def clean_module(self):
        """Si el usuario ya existe, evitar que se cambie el módulo."""
        module = self.cleaned_data.get('module')
        if self.instance.pk:  # Si el usuario ya está registrado
            return self.instance.module  # Mantener el módulo original
        return module

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Encripta la contraseña

        if commit:
            user.save()
        return user
class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'cargo', 'module']

    def __init__(self, *args, **kwargs):
        super(CustomUserEditForm, self).__init__(*args, **kwargs)

        # Hace que los campos sean opcionales
        for field in self.fields:
            self.fields[field].required = False

        # Agrega clases CSS
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Correo electrónico'})
        self.fields['role'].widget.attrs.update({'class': 'form-select'})
        self.fields['module'].widget.attrs.update({'class': 'form-select'})
        self.fields['cargo'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Cargo'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return self.instance.email  # Mantiene el valor anterior si no se cambia
        return email