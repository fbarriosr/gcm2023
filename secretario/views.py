from typing import Any
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
from django.contrib.auth.decorators import login_required

from django.shortcuts import HttpResponse
from datetime import datetime
from web.models import *
from socios.models import *
from web.mixins import *

nameWeb = "CGM"

class bus(SecretarioMixin, TemplateView):
    template_name = "secretario/views/bus.html"
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb

        contexto["title"] = "BUS"
        front = Front.objects.filter(titulo="bus")
        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        torneoid = self.request.COOKIES.get('torneo') 
        contexto['listado'] = Solicitud.objects.filter(torneo__id=torneoid).filter(estado = 'A').filter(busCGM= True).order_by('usuario__apellido_paterno')
        return contexto

class auto(SecretarioMixin, TemplateView):
    template_name = "secretario/views/auto.html"
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb

        contexto["title"] = "AUTO"
        front = Front.objects.filter(titulo="auto")
        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        torneoid = self.request.COOKIES.get('torneo') 
        contexto['listado'] = Solicitud.objects.filter(torneo__id=torneoid).filter(estado = 'A').filter(auto= True).order_by('usuario__apellido_paterno')
        return contexto
