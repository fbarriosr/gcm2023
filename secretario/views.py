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
import csv
from django.core.paginator import Paginator


nameWeb = "CGM"

def export_csv_bus(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="listado_bus.csv"'

    writer = csv.writer(response)
    writer.writerow(['Apellido Paterno', 'Apellido Materno', 'Primer Nombre', 'Segundo Nombre'])

    torneoid = request.COOKIES.get('torneo') 
    sol = Solicitud.objects.filter(torneo__id=torneoid).filter(estado = 'A').filter(busCGM= True).order_by('usuario__apellido_paterno')
       
    for obj in sol:
        writer.writerow([obj.usuario.apellido_paterno, obj.usuario.apellido_materno , obj.usuario.primer_nombre , obj.usuario.segundo_nombre ])

    return response

def export_csv_auto(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="listado_auto.csv"'

    writer = csv.writer(response)
    writer.writerow(['Apellido Paterno', 'Apellido Materno', 'Primer Nombre', 'Segundo Nombre', 'Patente'])

    torneoid = request.COOKIES.get('torneo') 
    sol = Solicitud.objects.filter(torneo__id=torneoid).filter(estado = 'A').filter(auto= True).order_by('usuario__apellido_paterno')
       
    for obj in sol:
        writer.writerow([obj.usuario.apellido_paterno, obj.usuario.apellido_materno , obj.usuario.primer_nombre , obj.usuario.segundo_nombre , obj.patente ])

    return response

class bus(SecretarioMixin, TemplateView):
    template_name = "secretario/views/bus.html"
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb

        contexto["title"] = "BUS"
        contexto['rol'] = self.request.user.perfil.perfil
        front = Front.objects.filter(titulo="bus")
        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        torneoid = self.request.COOKIES.get('torneo') 
        listado = Solicitud.objects.filter(torneo__id=torneoid).filter(estado = 'A').filter(busCGM= True).order_by('usuario__apellido_paterno')
        paginator = Paginator(listado,1)
        page = self.request.GET.get('page')
        contexto['datos']= paginator.get_page(page)

        return contexto

class auto(SecretarioMixin, TemplateView):
    template_name = "secretario/views/auto.html"
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb

        contexto["title"] = "AUTO"
        front = Front.objects.filter(titulo="auto")
        contexto['rol'] = self.request.user.perfil.perfil
        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        torneoid = self.request.COOKIES.get('torneo') 
        listado = Solicitud.objects.filter(torneo__id=torneoid).filter(estado = 'A').filter(auto= True).order_by('usuario__apellido_paterno')
        paginator = Paginator(listado,1)
        page = self.request.GET.get('page')
        contexto['datos']= paginator.get_page(page)
        return contexto
