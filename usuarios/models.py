import uuid
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
from search_admin_autocomplete.admin import SearchAutoCompleteAdmin
from .choices import *
from socios.choices import *
import datetime

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
    email                   = models.EmailField(verbose_name="email", max_length=255, unique=False, null=True)
    is_active               = models.BooleanField(default= True)  # para ingresar al login
    is_admin                = models.BooleanField(default= False) # para ingresar al admin
    rut                     = models.CharField(max_length=12,  unique=True, verbose_name="Rut")
    primer_nombre           = models.CharField(max_length=200, blank=True, null=False, verbose_name="Primer nombre")
    segundo_nombre          = models.CharField(max_length=200, blank=True, null=True, verbose_name="Segundo nombre")
    apellido_paterno        = models.CharField(max_length=200, blank=True, null=False, verbose_name="Apellido paterno")
    apellido_materno        = models.CharField(max_length=200, blank=True, null=False, verbose_name="Apellido materno")
    fecha_nacimiento        = models.DateField(blank=True, null=True, verbose_name="Fecha de nacimiento")
    telefono                = models.CharField(max_length=200,blank=True, null=True, verbose_name="Celular")
    sexo                    = models.CharField(max_length=1, choices=sexos, default="M", verbose_name="Genero")
    eCivil                  = models.CharField(max_length=30, choices=civil, default="NI", verbose_name="Estado Civil")  
    perfil                  = models.CharField(max_length=20, choices=perfil, default="S") # ej. socio,invitado, capitan, tesorero...
    estado                  = models.CharField(max_length=20, choices=estado, default="A")  # en que estado se encuentra la cuenta ej. activa, inactiva, suspendida
    categoria               = models.CharField(max_length=20, choices=categoria, default="NI")  # en que estado se encuentra la cuenta ej. activa, inactiva, suspendida
    situacionEspecial       = models.BooleanField(default=False, verbose_name="Situación Especial")
    fundador                = models.BooleanField(default=False, verbose_name="Fundador")

    institucion             = models.CharField(max_length=20, choices=instituciones, default="NI",blank=True)  # en que estado se encuentra la cuenta ej. activa, inactiva, suspendida
    grado                   = models.CharField(max_length=5, choices=grados, default="NI", blank=True)  # en que estado se encuentra la cuenta ej. activa, inactiva, suspendida
    condicion               = models.CharField(max_length=20, choices=condicion, default="NI", blank=True)  # en que estado se encuentra la cuenta ej. activa, inactiva, suspendida

    profesion               = models.CharField(max_length=200, blank=True, null=True, verbose_name="Profesión")
    fecha_incorporacion     = models.DateField(blank=True, null=True, default=datetime.date.today, verbose_name="Fecha de incorporacion")


    direccion       = models.CharField(max_length=200, blank=True, null= True, verbose_name="Direccion")
    region          = models.CharField(max_length=50,choices= regiones, blank=True, default= ' ', verbose_name="Region")
    
    tiempoGracia    = models.IntegerField(default=30, verbose_name="Tiempo Gracia")

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
