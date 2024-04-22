from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django import forms
from socios.models import *


class FormularioSolicitudViewTesorero(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
        			'deuda_socio','recargo','cuota','monto','cancela_deuda_socio',
                    'estado', 'motivo','suspende', 'motivoSuspencion']
        labels = {
            'usuario':'Usuario',
            'torneo': 'Torneo',
            'fecha': 'Fecha',
            'deuda_socio':'Deudas',
            'recargo':'Recargo',
            'cuota': 'Cuota de Campeonato',
            'cancela_deuda_socio': 'Cancela Deuda socio (NO/SI)',
            'monto': 'TOTAL',
            'estado': 'Estado',
            'motivo': 'Motivo',
            'suspende': 'Suspende',
            'motivoSuspencion': 'Motivo Suspención'
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
                    'rol': 'switch', 
                    'disabled': True

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
            'estado': forms.Select(
                attrs={
                    'class': 'form-control ',
                    'choices': estado_solicitud,
                    'id': 'estado',
                }
            ),
            'motivo': forms.Textarea(
                attrs = {
                    'class': 'form-control ',
                    'id': 'motivo',
                    'style': "height: 200px",
                }                
            ),
            'suspende': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input switch',
                    'id': 'suspende',
                    'type':'checkbox',
                    'rol': 'switch',
                    'disabled': True

                }                
            ),
            'motivoSuspencion': forms.Textarea(
                attrs = {
                    'class': 'form-control ',
                    'id': 'motivoSuspencion',
                    'readonly':''
                }                
            ),
        }

class FormularioSolicitudUpdateTesorero(FormularioSolicitudViewTesorero):
    def save(self,commit = True):
        user = super().save(commit = False)
        if commit:
            user.save()
        return user