from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import (
    View,
    TemplateView,
    ListView,
    UpdateView,
    CreateView,
    DeleteView,
    DetailView,
)
from .models import *
from django.core.paginator import Paginator

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy

from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse

from django.utils import timezone

from .forms import *
from datetime import timedelta, date
from socios.models import Parametro  # Importar la clase Parametro

nameWeb = "CGM"

class Login(FormView):
    
    template_name = 'usuarios/views/login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('inicio')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()

        # Verificar el estado del usuario
        if user.estado not in ['A', 'H', 'C']:  # Activo, Honorario, Cooperador
            if user.estado == 'S':
                return self.form_invalid(form, error_message="Tu cuenta está suspendida. Contacta al administrador.")
            elif user.estado == 'F':
                return self.form_invalid(form, error_message="Tu cuenta está marcada como fallecido. Contacta al administrador.")
            elif user.estado == 'PCS':
                return self.form_invalid(form, error_message="Has perdido la categoría de socio. Contacta al administrador.")

        # Obtener el parámetro de la edad máxima para "Socio Vitalicio"
        try:
            parametro_edad = Parametro.objects.get(tipo="edad_maxima_vitalicio")
            edad_maxima_vitalicio = int(parametro_edad.valor)
        except Parametro.DoesNotExist:
            edad_maxima_vitalicio = 80  # Valor por defecto si no se encuentra el parámetro

        # Calcular la edad del usuario con manejo de excepciones
        try:
            if user.fecha_nacimiento:
                edad = (date.today() - user.fecha_nacimiento).days // 365  # Aproximando a años
            else:
                edad = 0  # Si no hay fecha de nacimiento, se considera la edad como 0
        except (TypeError, ValueError) as e:
            edad = 0  # Si hay un error, se considera la edad como 0
            print(f"Error al calcular la edad del usuario: {e}")

        # Si el usuario es "Socio" y tiene más de la edad máxima, convertirlo en "Socio Vitalicio"
        if user.perfil == 'S' and edad > edad_maxima_vitalicio:
            user.perfil = 'S_V'  # Cambiar a 'Socio Vitalicio'
            user.save()  # Guardar el usuario para aplicar el cambio

        # Si el usuario es "Socio Vitalicio" y ya no cumple con la edad, volverlo a "Socio"
        elif user.perfil == 'S_V' and edad <= edad_maxima_vitalicio:
            user.perfil = 'S'  # Cambiar a "Socio" normal
            user.save()  # Guardar el usuario para aplicar el cambio

        # Verificar el tiempo de gracia
        if user.perfil == 'I' or user.perfil == 'I_E':
            diferencia_dias = (date.today() - user.fecha_incorporacion).days
            if user.tiempoGracia < diferencia_dias:
                return self.form_invalid(form, error_message="Se venció tu tiempo de gracia.", grace_period_expired=True)

        # Si pasa la validación, se procede al login
        login(self.request, user)
        return super(Login, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        contexto = super(Login, self).get_context_data(**kwargs)

        contexto['nameWeb'] = nameWeb
        contexto['title'] = 'ACCESO AL CLUB' 
        contexto['loginClass'] = 'loginClass'
        contexto['error'] = False
        contexto['grace_period_expired'] = False  # Valor por defecto

        return self.render_to_response(contexto)

    def form_invalid(self, form, error_message="Error en el login", grace_period_expired=False, **kwargs):
        contexto = super(Login, self).get_context_data(**kwargs)
        contexto['nameWeb'] = nameWeb
        contexto['title'] = 'Error'
        contexto['loginClass'] = 'loginClass'
        contexto['error'] = True
        contexto['grace_period_expired'] = grace_period_expired  # Para diferenciar errores
        contexto['error_message'] = error_message  # Mensaje personalizado
        return self.render_to_response(contexto)

def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login')