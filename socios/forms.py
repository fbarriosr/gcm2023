from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django import forms
from .models import *


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
