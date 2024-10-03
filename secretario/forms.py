from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django import forms
from .models import *
from socios.models import *
from usuarios.choices import grados, instituciones
from web.models import *
from datetime import datetime
from django_recaptcha.fields import ReCaptchaField

from socios.choices import regiones
from usuarios.choices import *

class FormularioRankingUpdate(forms.ModelForm):
    class Meta:
        model = Paginas_Socio
        fields = ['contenido','file']
        labels = {
            'contenido':'Contenido',
            'file': 'Archivo'
        }
        widgets = {
            'contenido': forms.Textarea(
                attrs = {
                    'class': 'form-control ',
                    'id': 'descripcion',
                    'style': "height: 200px",
                }                
            ),
            'file': forms.FileInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'file',
                }                
            ),
        }

    def save(self,commit = True):
        user = super().save(commit = False)
        if commit:
            user.save()
        return user



class FormularioNoticiaCreate(forms.ModelForm):
    img_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}))
    
    class Meta:
        model = Noticia
        fields = ['titulo', 'fecha', 'resumen', 'info', 'direccion', 'region', 'img', 'img_files']
        labels = {
            'titulo': 'Titulo (requerido)',
            'fecha': 'Fecha (requerido)',
            'resumen': 'Resumen (requerido)',
            'info': 'Información (requerido)',
            'direccion': 'Dirección',
            'region': 'Región (requerido)',
            'img': 'Imagen Principal'
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'id': 'titulo'}),
            'fecha': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 'placeholder': 'Selecciona una fecha', 'type': 'date'}
            ),
            'resumen': forms.TextInput(attrs={'class': 'form-control', 'id': 'resumen'}),
            'info': forms.Textarea(attrs={'class': 'form-control', 'id': 'info', 'style': 'height: 200px'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'id': 'direccion'}),
            'region': forms.Select(attrs={'class': 'form-control', 'id': 'region'}),
            'img': forms.FileInput(attrs={'class': 'form-control', 'id': 'img'}),
        }


class FormularioNoticiaUpdate(FormularioNoticiaCreate):
    img_files = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}))
    
    class Meta:
        model = Noticia
        fields = ['titulo', 'fecha', 'resumen', 'info', 'direccion', 'region', 'img', 'img_files', 'is_active']
        labels = {
            'titulo': 'Titulo (requerido)',
            'fecha': 'Fecha (requerido)',
            'resumen': 'Resumen (requerido)',
            'info': 'Información (requerido)',
            'direccion': 'Dirección',
            'region': 'Región (requerido)',
            'img': 'Imagen Principal',
            'is_active': 'Activo'
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'id': 'titulo'}),
            'fecha': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 'placeholder': 'Selecciona una fecha', 'type': 'date'}
            ),
            'resumen': forms.TextInput(attrs={'class': 'form-control', 'id': 'resumen'}),
            'info': forms.Textarea(attrs={'class': 'form-control', 'id': 'info', 'style': 'height: 200px'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'id': 'direccion'}),
            'region': forms.Select(attrs={'class': 'form-control', 'id': 'region'}),
            'img': forms.FileInput(attrs={'class': 'form-control', 'id': 'img'}),
            'is_active': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input switch',
                    'id': 'is_active',
                    'type':'checkbox',
                    'rol': 'switch'

                }                
            )
        }



class FormularioMultimediaCreate(forms.ModelForm):
    img_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}))
    
    class Meta:
        model = Multimedia
        fields = ['titulo', 'fecha', 'img', 'img_files']
        labels = {
            'titulo': 'Titulo (requerido)',
            'fecha': 'Fecha (requerido)',
            'img': 'Imagen Principal'
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'id': 'titulo'}),
            'fecha': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 'placeholder': 'Selecciona una fecha', 'type': 'date'}
            ),
            'img': forms.FileInput(attrs={'class': 'form-control', 'id': 'img'}),
        }


class FormularioMultimediaUpdate(FormularioMultimediaCreate):
    img_files = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}))
    
    class Meta:
        model = Multimedia
        fields = ['titulo', 'fecha',  'img', 'img_files', 'is_active']
        labels = {
            'titulo': 'Titulo (requerido)',
            'fecha': 'Fecha (requerido)',
            'img': 'Imagen Principal',
            'is_active': 'Activo'
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'id': 'titulo'}),
            'fecha': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 'placeholder': 'Selecciona una fecha', 'type': 'date'}
            ),
            'img': forms.FileInput(attrs={'class': 'form-control', 'id': 'img'}),
            'is_active': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input switch',
                    'id': 'is_active',
                    'type':'checkbox',
                    'rol': 'switch'

                }                
            )
        }

class FormularioTorneoCreate(forms.ModelForm):
    class Meta:
        model = Torneo
        fields = [ 'titulo','fecha' ,'direccion','region',                     
                    'cupos','activo','actual','abierto',
                    'bases','list_salidas','resultados',     
                    'premiacion', 'galeria', 'ticket', 'recargo','ticket_inv', 'ticket_bus' ]
        labels = {
            'titulo'        : 'Titulo (requerido) ',
            'fecha'         : 'Fecha (requerido)',        
            'direccion'     : 'Dirección (requerido)',       
            'region'        : 'Región (requerido)',      
            'cupos'         : 'Cupos (requerido)',
            'activo'        : 'Ver Torneo (No/Si)', 
            'actual'        : 'Torneo Actual (No/Si)',  
            'abierto'       : 'Torneo Abierto (No/Si)',   
            'bases'         : 'Bases', 
            'list_salidas'  : 'Listado de Salidas',
            'resultados'    : 'Resultados',
            'premiacion'    : 'Premiación',
            'galeria'       : 'Galeria',
            'ticket'        : 'Inscripción Campeonato',
            'recargo'       : 'Recargo (Socio)',
            'ticket_inv'    : 'Recargo (Invitado)',
            'ticket_bus'    : 'Ticket Bus',
        }
        widgets = {
            'titulo': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'titulo',
                }                
            ),
            'fecha':forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
                       'placeholder': 'Select a date',
                       'type': 'date'
                      }
            ),
            'direccion': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'direccion',
                }                
            ),
            'region': forms.Select(
                attrs={
                    'class': 'form-control ',
                    'choices': regiones,
                    'id': 'region',
                }
            ),
            'cupos': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'cupos',
                }                
            ),
            'ticket': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'ticket',
                }                
            ),
            'recargo': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'recargow',
                }                
            ),
            'ticket_inv': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'ticket_inv',
                }                
            ),
            'ticket_bus': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'ticket_bus',
                }                
            ),
            'activo': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input switch',
                    'id': 'activo',
                    'type':'checkbox',
                    'rol': 'switch'

                }                
            ),
            'actual': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input switch',
                    'id': 'actual',
                    'type':'checkbox',
                    'rol': 'switch'

                }                
            ),
            'abierto': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input switch',
                    'id': 'abierto',
                    'type':'checkbox',
                    'rol': 'switch'

                }                
            ),
            'bases': forms.FileInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'bases',
                }                
            ),

            'list_salidas': forms.FileInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'list_salidas',
                }                
            ),
            'resultados': forms.FileInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'resultados',
                }                
            ),
            'premiacion': forms.FileInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'premiacion',
                }                
            ),
            'galeria': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'galeria',
                }                
            )

        }


class FormularioTorneoUpdate(FormularioTorneoCreate):
    def save(self,commit = True):
        user = super().save(commit = False)
        if commit:
            user.save()
        return user


class FormularioTorneoUpdateCapitan(forms.ModelForm):
    class Meta:
        model = Torneo
        fields = [ 'titulo','fecha' ,                     
                    'list_salidas','resultados', 'premiacion' ]
        labels = {
            'titulo'        : 'Titulo (requerido) ',
            'fecha'         : 'Fecha (requerido)',            
            'list_salidas'  : 'Listado de Salidas',
            'resultados'    : 'Resultados',
            'premiacion'    : 'Premiación',
        }
        widgets = {
            'titulo': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'titulo',
                    'readonly':''
                }                
            ),
            'fecha':forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
                       'placeholder': 'Select a date',
                       'type': 'date',
                       'readonly':''
                      }
            ),
            'list_salidas': forms.FileInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'list_salidas',
                }                
            ),
            'resultados': forms.FileInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'resultados',
                }                
            ),
            'premiacion': forms.FileInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'premiacion',
                }                
            ),
        }




    
class FormularioUsuariosView(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['primer_nombre','segundo_nombre','apellido_paterno','apellido_materno',
                    'rut','email','telefono', 'region','direccion','fecha_nacimiento',
                    'estado','categoria','sexo','eCivil','perfil','situacionEspecial','fundador',
                    "is_admin",'is_active','tiempoGracia',
                    'institucion','grado','profesion', 'condicion','fecha_incorporacion' ]
        labels = {
            'primer_nombre':'Primer Nombre',
            'segundo_nombre': 'Segundo Nombre',
            'apellido_paterno': 'Apellido Paterno',
            'apellido_materno': 'Apellido Materno',
            'rut':  'RUT',
            'email': 'Correo electrónico',
            'telefono':'Telefono',
            'region':'Región',
            'direccion':'Dirección',
            'sexo': 'Sexo',
            'eCivil': 'Estado Civil',
            'perfil': 'Perfil',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'estado' :'Estado',
            'situacionEspecial': 'Situacion Especial',
            'fundador':'Fundador',
            "is_admin": 'is_admin',
            'is_active': 'is_active',
            'tiempoGracia': 'tiempoGracia',
            'categoria': 'Categoria',
            'institucion': 'Institucion',
            'grado':'Grado',
            'profesion':'Profesion',
            'condicion': 'Condicion',
            'fecha_incorporacion': 'Fecha de Incorporacion'
        }
        widgets = {

            'primer_nombre': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'primer_nombre',
                }                
            ),
            'segundo_nombre': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'segundo_nombre',
                }                
            ),
            'apellido_paterno': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'apellido_paterno',
                }                
            ),
            'apellido_materno': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'apellido_materno'
                }                
            ),

            'rut': forms.TextInput(
                attrs={
                    'class': 'form-control ',
                    'id': 'rut',
                   
                }
            ),
           
            'fecha_nacimiento': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
                       'placeholder': 'Select a date',
                       'type': 'date'
                      }
            ),

            'email': forms.EmailInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'email',
                    'value':'@gmail.com',
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'class': 'form-control ',
                    'id': 'telefono',
                    'value':'+56 9 ',
                }
            ),
            'region': forms.Select(
                attrs={
                    'class': 'form-control ',
                    'choices': regiones,
                    'id': 'region',
                }
            ),
            'direccion': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'direccion',
                }                
            ),
            'sexo': forms.Select(
                attrs={
                    'class': 'form-control ',
                    'choices': sexos,
                    'id': 'sexo',
                }
            ),
            'eCivil': forms.Select(
                attrs={
                    'class': 'form-control ',
                    'choices': civil,
                    'id': 'eCivil',
                }
            ),
            'estado': forms.Select(
                attrs={
                    'class': 'form-control ',
                    'choices': estado,
                    'id': 'estado',
                }
            ),
            'perfil': forms.Select(
                attrs={
                    'class': 'form-control ',
                 
                    'id': 'perfil',
                }
            ),
            'categoria': forms.Select(
                attrs={
                    'class': 'form-control ',
                    'choices': categoria,
                    'id': 'categoria',
                }
            ),
            'fundador': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input switch',
                    'id': 'fundador',
                    'type':'checkbox',
                    'rol': 'switch'

                }                
            ),
            'situacionEspecial': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input switch',
                    'id': 'situacionEspecial',
                    'type':'checkbox',
                    'rol': 'switch'

                }                
            ),
            'tiempoGracia': forms.TextInput(
                attrs={
                    'class': 'form-control ',
                    'id': 'tiempoGracia',
                }
            ),

            'is_active': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input switch',
                    'id': 'is_active',
                    'type':'checkbox',
                    'rol': 'switch'

                }                
            ),
            'is_admin': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input switch',
                    'id': 'is_admin',
                    'type':'checkbox',
                    'rol': 'switch'

                }                
            ),
            'institucion': forms.Select(
                attrs={
                    'class': 'form-control ',
                    'choices': instituciones,
                    'id': 'institucion',
                
                }
            ),
            'grado':  forms.Select(
                attrs={
                    'class': 'form-control ',
                    'choices': grados,
                    'id': 'grados',
                
                }),
            'condicion': forms.Select(
                attrs={
                    'class': 'form-control ',
                    'choices': condicion,
                    'id': 'condicion',
                }
            ),
            'profesion': forms.TextInput(
                attrs={
                    'class': 'form-control ',
                    'id': 'profesion',
                }
            ),
            'fecha_incorporacion': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
                       'placeholder': 'Select a date',
                       'type': 'date'
                      }
            ),
        }

    def save(self,commit = True):
        user = super().save(commit = False)
        if commit:
            user.save()
        return user

    def save(self,commit = True):
        user = super().save(commit = False)
        if commit:
            user.save()
        return user   

