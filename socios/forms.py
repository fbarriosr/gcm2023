from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django import forms
from .models import *
from datetime import datetime

class FormularioSolicitudView(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['indice','auto','patente','busCGM','carro','descripcion',
                    'acompanantes','deuda_socio','recargo','cuota','monto','cancela_deuda_socio']
        labels = {
            'usuario':'Usuario',
            'torneo': 'Torneo',
            'fecha': 'Fecha',
            'auto': '¿Vas en auto?',
            'patente': 'Registre la Patente',
            'busCGM':'¿Usará BUS CGM? (NO/SI)',
            'carro': '¿Participará en Carro? (NO/SI)',
            'indice':'Ingrese su Índice',
            'acompanantes':'¿Con quien va?',
            'descripcion':'Solicitud',
            'deuda_socio':'Deudas',
            'recargo':'Recargo',
            'cuota': 'Cuota de Campeonato',
            'cancela_deuda_socio': 'Cancela Deuda socio (NO/SI)',
            'monto': 'TOTAL'

        }
        widgets = {

            'usuario': forms.EmailInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'usuario',
                    'value':'@wtos.cl',
                    'readonly':''
                }
            ),
            'torneo': forms.TextInput(
                attrs={
                    'class': 'form-control ',
                    'id': 'torneo',
                    'readonly':''
                }
            ),
            'fecha': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'fecha',
                    'readonly':''
                }                
            ),
            'auto': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input switch',
                    'id': 'auto',
                    'type':'checkbox',
                    'rol': 'switch'

                }                
            ),
            'patente': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'patente',
                }                
            ),
            'busCGM': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input switch',
                    'id': 'busCGM',
                    'type':'checkbox',
                    'rol': 'switch'

                }                
            ),
            
            'carro': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input switch',
                    'id': 'carro',
                    'type':'checkbox',
                    'rol': 'switch'

                }                
            ),
            
            'indice': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'indice',
                }                
            ),
            'acompanantes': forms.Textarea(
                attrs = {
                    'class': 'form-control ',
                    'id': 'acompanantes',
                }                
            ),
            'descripcion': forms.Textarea(
                attrs = {
                    'class': 'form-control ',
                    'id': 'descripcion',
                    'style': "height: 200px",
                }                
            ),
            'deuda_socio': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'deuda',
                    'readonly':''
                    
                }                
            ),
            'recargo': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'recargo',
                    'readonly':''
                }                
            ),
            'cuota': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'cuota',
                    'readonly':''
                }                
            ),
            'cancela_deuda_socio': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input switch',
                    'id': 'cancela_deuda_socio',
                    'type':'checkbox',
                    'rol': 'switch'

                }                
            ),
            'monto': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'total',
                    'style':'font-weight: bolder; font-size: 24px;',
                    'readonly':''
                }                
            ),
        }

class FormularioSolicitudCreate(FormularioSolicitudView):
    def save(self,commit = True):
        user = super().save(commit = False)
        if commit:
            user.save()
        return user


class FormularioSolicitudSuspenderCreate(FormularioSolicitudCreate):
    class Meta:
        model = Solicitud
        fields = ['motivoSuspencion']
        labels = {
            'motivoSuspencion': 'Motivo'
        }
        widgets = {
                    'motivoSuspencion': forms.Textarea(
                                    attrs = {
                                        'class': 'form-control ',
                                        'id': 'motivoSuspencion',
                                        'style': "height: 200px",
                                    }                
                                ),
                  }



class FormularioPerfilUpdate(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['primer_nombre','segundo_nombre','apellido_paterno','apellido_materno',
                    'rut','email','telefono', 'fecha_nacimiento',
                    'institucion','grado','profesion' ]
        labels = {
            'primer_nombre':'Primer Nombre',
            'segundo_nombre': 'Segundo Nombre',
            'apellido_paterno': 'Apellido Paterno',
            'apellido_materno': 'Apellido Materno',
            'rut':  'RUT',
            'email': 'Correo electrónico',
            'telefono':'Telefono',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'institucion': 'Institucion',
            'grado':'Grado',
            'profesion':'Profesion'
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
                    'readonly':''
                }
            ),
           
            'fecha_nacimiento': forms.TextInput(
                attrs={
                    'class': 'form-control ',
                    'id': 'fecha_nacimiento',
                    'readonly':''
                }
            ),

            'email': forms.EmailInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'email',
                    'value':'@wtos.cl',
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'class': 'form-control ',
                    'id': 'telefono',
                    'readonly':''
                }
            ),
            'institucion': forms.TextInput(
                attrs={
                    'class': 'form-control ',
                    'id': 'institucion',
                    'readonly':''
                }
            ),
            'grado': forms.TextInput(
                attrs={
                    'class': 'form-control ',
                    'id': 'grado',
                    'readonly':''
                }
            ),
            'profesion': forms.TextInput(
                attrs={
                    'class': 'form-control ',
                    'id': 'profesion',
                }
            ),
        }

    def save(self,commit = True):
        user = super().save(commit = False)
        if commit:
            user.save()
        return user




class FormularioUsuarioPassword(forms.ModelForm):
    """ Formulario de Registro de un Usuario en la base de datos
    Variables:
        - password1:    Contraseña
        - password2:    Verificación de la contraseña
    """
    password1 = forms.CharField(label = 'Contraseña',widget = forms.PasswordInput(
        attrs = {
            'class': 'form-control progressPassword',
            'placeholder': 'Ingrese su contraseña...',
            'id': 'password1',
            'required':'required',
        }
    ),validators=[validate_password])

    password2 = forms.CharField(label = 'Contraseña de Confirmación', widget = forms.PasswordInput(
        attrs={
            'class': 'form-control ',
            'placeholder': 'Ingrese nuevamente su contraseña...',
            'id': 'password2',
            'required': 'required',
        }
    ),validators=[validate_password])

    class Meta:
        model = Usuario
        fields = ('password1','password2')
        

    def clean_password2(self):
        """ Validación de Contraseña
        Metodo que valida que ambas contraseñas ingresadas sean igual, esto antes de ser encriptadas
        y guardadas en la base dedatos, Retornar la contraseña Válida.
        Excepciones:
        - ValidationError -- cuando las contraseñas no son iguales muestra un mensaje de error
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Contraseñas no coinciden!')
        return password2

    def save(self,commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
        