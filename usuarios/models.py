import uuid
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
from search_admin_autocomplete.admin import SearchAutoCompleteAdmin
from .choices import *
import datetime

class Perfil(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    perfil = models.CharField(
        max_length=30, blank=False, null=False, verbose_name="Perfil de usuario"
    )
    descripcion = models.TextField(
        blank=True, null=True, verbose_name="Descripcion del perfil"
    )
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
        ordering = ["order"]

    def __str__(self):
        return self.perfil


class PerfilAdmin(SearchAutoCompleteAdmin, admin.ModelAdmin):
    search_fields = ["perfil"]
    list_display = ("perfil", "order")
    list_per_page = 10


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser):
    email                   = models.EmailField(verbose_name="email", max_length=255, unique=True)
    is_active               = models.BooleanField(default=True)
    is_admin                = models.BooleanField(default=False)
    rut                     = models.CharField(max_length=12,  unique=True, verbose_name="Rut")
    primer_nombre           = models.CharField(max_length=200, blank=True, null=False, verbose_name="Primer nombre")
    segundo_nombre          = models.CharField(max_length=200, blank=True, null=False, verbose_name="Segundo nombre")
    apellido_paterno        = models.CharField(max_length=200, blank=True, null=False, verbose_name="Apellido paterno")
    apellido_materno        = models.CharField(max_length=200, blank=True, null=False, verbose_name="Apellido materno")
    fecha_nacimiento        = models.DateField(blank=True, null=True, verbose_name="Fecha de nacimiento")
    telefono                = models.IntegerField(blank=True, null=True, verbose_name="Celular")
    sexo                    = models.CharField(max_length=1, choices=sexos, default="M", verbose_name="Genero")
    eCivil                  = models.CharField(max_length=30, choices=civil, default="NI", verbose_name="Estado Civil")  
    perfil                  = models.ForeignKey(Perfil, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Perfil de usuario")  # ej. socio,invitado, capitan, tesorero...
    estado                  = models.CharField(max_length=20, choices=estado, default="A")  # en que estado se encuentra la cuenta ej. activa, inactiva, suspendida
    categoria               = models.CharField(max_length=20, choices=categoria, default="N")  # en que estado se encuentra la cuenta ej. activa, inactiva, suspendida
    situacionEspecial       = models.BooleanField(default=False, verbose_name="Situación Especial")
    fundador                = models.BooleanField(default=False, verbose_name="Fundador")

    institucion             = models.CharField(max_length=20, choices=instituciones, default="NI")  # en que estado se encuentra la cuenta ej. activa, inactiva, suspendida
    grado                   = models.CharField(max_length=5, choices=grados, default="NI")  # en que estado se encuentra la cuenta ej. activa, inactiva, suspendida
    condicion               = models.CharField(max_length=20, choices=condicion, default="NI")  # en que estado se encuentra la cuenta ej. activa, inactiva, suspendida

    profesion               = models.CharField(max_length=200, blank=True, null=False, verbose_name="Profesión")
    fecha_incorporacion     = models.DateField(default=datetime.date.today)
    objects = MyUserManager()

    USERNAME_FIELD = "rut"
    REQUIRED_FIELDS = ["email",'apellido_paterno','primer_nombre']

    def __str__(self):
        return self.rut

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
