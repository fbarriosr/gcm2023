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
from web.models import *
from socios.models import *
from usuarios.models import *
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


from django.shortcuts import HttpResponse
from datetime import datetime
#from .forms import *

from datetime import datetime
import csv
import calendar


nameWeb = "CGM"


def export_csv_cumpleanos(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="listado_cumpleanos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Apellido Paterno', 'Apellido Materno', 'Primer Nombre', 'Segundo Nombre', 'Fecha', 'Grado', 
        'Institucion', 'Fundador','Estado', 'Perfil','Telefono'])

    sol = Usuario.objects.order_by('fecha_nacimiento__month', 'fecha_nacimiento__day')
       
    for obj in sol:
        writer.writerow([ obj.apellido_paterno.capitalize(), obj.apellido_materno.capitalize() , obj.primer_nombre.capitalize() , obj.segundo_nombre.capitalize() , 
            obj.fecha_nacimiento, obj.get_grado_display(), obj.get_institucion_display(), obj.fundador , obj.get_estado_display(), obj.perfil , obj.telefono ])

    return response


def export_csv_cumpleanos_mes(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="listado_cumpleanos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Apellido Paterno', 'Apellido Materno', 'Primer Nombre', 'Segundo Nombre', 'Fecha', 'Grado', 
        'Institucion', 'Fundador','Estado', 'Perfil','Telefono'])

    fecha = datetime.now()
    month = fecha.month

    sol = Usuario.objects.filter( 
                      fecha_nacimiento__month=month).order_by('fecha_nacimiento__day')
       
    for obj in sol:
        writer.writerow([ obj.apellido_paterno.capitalize(), obj.apellido_materno.capitalize() , obj.primer_nombre.capitalize() , obj.segundo_nombre.capitalize() , 
            obj.fecha_nacimiento, obj.get_grado_display(), obj.get_institucion_display(), obj.fundador , obj.get_estado_display(), obj.perfil , obj.telefono ])

    return response


class cumpleanos(TemplateView):
    template_name = "capitan/views/cumpleanos.html"
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb

        contexto["title"] = "CUMPLEAÑOS"
        front = Front.objects.filter(titulo="Cumpleaños")
        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        contexto['rol'] = self.request.user.perfil.perfil
        fecha = datetime.now()
        month = fecha.month
        contexto['mes']= calendar.month_name[month]

        listado = Usuario.objects.filter( 
                      fecha_nacimiento__month=month).order_by('fecha_nacimiento__day')
        
        paginator = Paginator(listado,1)
        page = self.request.GET.get('page')
        contexto['datos']= paginator.get_page(page)
        return contexto


