from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
)

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None):
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario')
        username = username.strip()
        email = self.normalize_email(email) if email else None

        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('Administrador', 'Administrador'),
        ('Empleado', 'Empleado'),
    ]
    
    MODULES = [
        ('Papeleria', 'Papelería'),
        ('Cafeteria', 'Cafetería'),
        ('Centro de eventos', 'Centro de eventos')
    ]
    username = models.CharField(max_length=100, unique=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    role = models.CharField(max_length=13, choices=ROLES, default='Empleado')
    cargo = models.CharField(max_length=30, default='No establecido')
    module = models.CharField(max_length=30, choices=MODULES, default='papeleria')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    def __str__(self):
        return self.username
    def get_module_display(self):
        """Devuelve el nombre legible del módulo."""
        return dict(self.MODULES).get(self.module, self.module)