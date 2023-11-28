from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class FormularioLogin(AuthenticationForm):
	def __init__(self,*args,**kwargs):
	    super(FormularioLogin,self).__init__(*args,**kwargs)
	    self.fields['username'].widget.attrs['class'] = 'form-control'
	    self.fields['username'].widget.attrs['placeholder'] = 'Usuario'
	    self.fields['username'].widget.attrs['label'] = 'Usuarios'


	    self.fields['password'].widget.attrs['class'] = 'form-control'
	    self.fields['password'].widget.attrs['placeholder'] = 'Ingrese Contraseña'
	    self.fields['password'].widget.attrs['label'] = 'Contraseñas'