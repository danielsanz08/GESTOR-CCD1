from django import forms
from papeleria.models import Articulo

from django.contrib.auth import authenticate
class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
class ArticuloForm(forms.ModelForm):
        class Meta:
            model = Articulo
            fields = ['nombre', 'marca', 'observacion', 'precio', 'cantidad',    'tipo']

class ArticuloEditForm(forms.ModelForm):    
    class Meta:
        model = Articulo
        fields = ['nombre', 'marca', 'observacion', 'precio', 'cantidad', 'tipo']
    def __init__(self, *args,**kwargs):
        super(ArticuloEditForm, self).__init__(*args, **kwargs)
        # Hace que los campos sean opcionales
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre del articulo'})
        self.fields['marca'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Marca del articulo'})
        self.fields['observacion'].widget.attrs.update({'class':'form-control', 'placeholder': 'Observación' })
        self.fields['precio'].widget.attrs.update({'class':'form-control', 'placeholder': 'Precio del  articulo'})
        self.fields['cantidad'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Cantidad de articulo'})
        self.fields['tipo'].widget.attrs.update({'class':'form-control', 'placeholder': 'Tipo de articulo'})
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Mantener valores anteriores si no se proporciona un nuevo valor
        for field in self.fields:
            if not cleaned_data.get(field):
                cleaned_data[field] = getattr(self.instance, field)

        return cleaned_data
