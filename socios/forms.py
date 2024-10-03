from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django import forms
from .models import *
from web.models import *
from usuarios.choices import grados, instituciones
from datetime import datetime
from django_recaptcha.fields import ReCaptchaField



class FormularioSolicitudView(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['indice','auto','patente','busCGM','carro',
                    'acompanantes','deuda_socio','recargo','recargo_invitado','recargo_bus','cuota','monto','cancela_deuda_socio', 'detalle_cuotas_pagadas']
        labels = {
            'usuario':'Usuario',
            'torneo': 'Torneo',
            'fecha': 'Fecha',
            'auto': '¿Necesita estacionamiento en Unidad Militar?',
            'patente': 'Registre la Patente',
            'busCGM':'¿Usará BUS CGM? (NO/SI)',
            'carro': '¿Participará en Carro? (NO/SI)',
            'indice':'Ingrese su Índice',
            'acompanantes':'¿Con quien va?',
            'deuda_socio':'Deudas ($CLP)',
            'recargo':'Recargo Deuda Socio($CLP)',
            'recargo_invitado':  'Recargo Invitado ($CLP)',
            'recargo_bus':  'Recargo BUS ($CLP)',
            'cuota': 'Cuota de Campeonato ($CLP)',
            'cancela_deuda_socio': 'Cancela Deuda socio (NO/SI)',
            'monto': 'Total($CLP)',
            'estado': 'Estado',
            'detalle_cuotas_pagadas': 'Detalle Cuotas Pendientes',
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
            'deuda_socio': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'deuda',
                    'readonly':''
                    
                }                
            ),
            'detalle_cuotas_pagadas': forms.Textarea(
                attrs = {
                    'class': 'form-control ',
                    'id': 'detalle_cuotas_pagadas',
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
            'recargo_invitado': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'recargo_invitado',
                    'readonly':''
                }                
            ),
            'recargo_bus': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'recargo_bus',
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
            )

        }

class FormularioSolicitudCreate(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['indice','auto','patente','busCGM','carro',
                    'acompanantes','deuda_socio','recargo','recargo_invitado','recargo_bus','cuota','monto','detalle_cuotas_pagadas']
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
            'deuda_socio':'Deudas',
            'recargo':'Recargo Deuda Socio($CLP)',
            'recargo_invitado':  'Recargo Invitado ($CLP)',
            'recargo_bus':  'Recargo BUS ($CLP)',
            'cuota': 'Cuota de Campeonato',
            'cancela_deuda_socio': 'Cancela Deuda socio (NO/SI)',
            'monto': 'TOTAL $ CLP: ',
            'detalle_cuotas_pagadas': 'Detalle Cuotas Pagadas'
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
            'recargo_invitado': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'recargo_invitado',
                    'readonly':''
                }                
            ),
            'recargo_bus': forms.TextInput(
                attrs = {
                    'class': 'form-control ',
                    'id': 'recargo_bus',
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
             'detalle_cuotas_pagadas ': forms.Textarea(
                attrs = {
                    'class': 'form-control ',
                    'id': 'detalle_cuotas_pagadas',
                    'readonly':''
                    
                }                
            ), 
            
        }
    def save(self,commit = True):
        user = super().save(commit = False)
        if commit:
            user.save()
        return user




class FormularioPerfilUpdate(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['primer_nombre','segundo_nombre','apellido_paterno','apellido_materno',
                    'rut','email','telefono', 'fecha_nacimiento',
                    'institucion','grado','profesion',
                    'region', 'direccion' ]
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
            'profesion':'Profesion',
            'region': 'Región',
            'direccion': 'Dirección'
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
                    'value':'@wtos.cl',
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'class': 'form-control ',
                    'id': 'telefono',
                }
            ),
            'institucion': forms.Select(
                attrs={
                    'class': 'form-control ',
                    'choices': instituciones,
                    'id': 'institucion',
                    'disabled':'disabled'
                }
            ),
            'grado':  forms.Select(
                attrs={
                    'class': 'form-control ',
                    'choices': grados,
                    'id': 'grados',
                    'disabled':'disabled'
                }),

            'profesion': forms.TextInput(
                attrs={
                    'class': 'form-control ',
                    'id': 'profesion',
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'class': 'form-control ',
                    'id': 'direccion',
                }
            ),
            'region':  forms.Select(
                attrs={
                    'class': 'form-control ',
                    'choices': regiones,
                    'id': 'region',
                }),
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
        


# Del formulario para generar_cuotas_form.html
class GenerarCuotasForm(forms.Form):
    año = forms.IntegerField(
        label='Ingrese el año:',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2024'})
    )
    valor = forms.DecimalField(
        label='Ingrese el valor de la cuota:',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '8000'})
    )
    descuento = forms.DecimalField(
        label='Ingrese el valor del descuento anual:',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '15000'})
    )
    cargo = forms.DecimalField(
        label='Ingrese el cargo por no pago:',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '4000'})
    )

class OperacionesCuotasForm(forms.Form):
    rut = forms.CharField(
        label='Ingrese su rut:',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '8000'})
    )
    
    año = forms.IntegerField(
        label='Ingrese el año:',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2024'})
    )


