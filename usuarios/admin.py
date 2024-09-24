from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from usuarios.models import *

from import_export.admin import ImportExportModelAdmin


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = Usuario
        fields = ["email" ,'is_admin','is_active']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField(label=("Password"),
        help_text=("Las contraseñas sin procesar no se almacenan, por lo que no hay forma de ver la "
                     "contraseña de este usuario. Pero puedes cambiar esta contraseña."
                     "Usando este formulario: <a href=\"../password/\">RESET PASSWORD</a>."))



    class Meta:
        model = Usuario
        fields = ["password", "email", "is_active", "is_admin"]

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(ImportExportModelAdmin,BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['rut','apellido_paterno','primer_nombre',"email",'perfil', 'condicion','estado','categoria','is_admin','situacionEspecial']
    list_filter = ['perfil','condicion', 'estado', 'categoria',"is_admin", 'situacionEspecial']
    fieldsets = [
        ('Principal', {"fields": ["rut",'password']}),
        ("Personal", {"fields": ['primer_nombre','segundo_nombre','apellido_paterno','apellido_materno',"email",'fecha_nacimiento']}),
        ('Info', {"fields": ["telefono",'region','direccion','sexo','eCivil','perfil','estado','categoria','situacionEspecial','fundador']}),
        ("Permisos", {"fields": ["is_admin",'is_active', 'tiempoGracia']}),
        ("Personal Uniformado", {"fields": ["institucion",'grado', 'condicion','profesion','fecha_incorporacion']}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        ('Datos', {"fields": ["rut", "password1",'password2']}),
        ("Personal", {"fields": ['primer_nombre','segundo_nombre','apellido_paterno','apellido_materno',"email",'fecha_nacimiento']}),
        ('Info', {"fields": ["telefono",'region','direccion','sexo','eCivil','perfil','estado','categoria','situacionEspecial','fundador']}),
        ("Permisos", {"fields": ["is_admin",'is_active','tiempoGracia']}),
        ("Personal Uniformado", {"fields": ["institucion",'grado', 'condicion','profesion','fecha_incorporacion']}),
    ]
    search_fields = ['apellido_paterno','rut','primer_nombre']
    ordering = ["apellido_paterno",'rut']
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(Usuario, UserAdmin )
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)