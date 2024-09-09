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

from .forms import *
from datetime import timedelta, date

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

        # Supongo que 'perfil', 'tiempoGracia' y 'fecha_incorporacion' son atributos del usuario
        if user.perfil == 'I':
            diferencia_dias = (date.today() - user.fecha_incorporacion).days
            if user.tiempoGracia < diferencia_dias:
                # Si el tiempo de gracia ha expirado, redirigir con error personalizado
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