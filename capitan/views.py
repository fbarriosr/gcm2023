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
from socios.mixins import *
from django.utils import timezone
from .choices import *
from secretario.forms import FormularioTorneoUpdateCapitan

nameWeb = "CGM"


def export_csv_cumpleanos(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="listado_cumpleanos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Apellido Paterno', 'Apellido Materno', 'Primer Nombre', 'Segundo Nombre', 'Fecha', 'Grado', 
        'Institucion', 'Fundador','Estado', 'Perfil','Telefono'])

    sol = Usuario.objects.order_by('fecha_nacimiento__month', 'fecha_nacimiento__day')
       
    for obj in sol:
        try:
            apellido_paterno = obj.apellido_paterno.capitalize()
        except AttributeError:
            apellido_paterno = ''

        try:
            apellido_materno = obj.apellido_materno.capitalize()
        except AttributeError:
            apellido_materno = ''

        try:
            primer_nombre = obj.primer_nombre.capitalize()
        except AttributeError:
            primer_nombre = ''

        try:
            segundo_nombre = obj.segundo_nombre.capitalize()
        except AttributeError:
            segundo_nombre = ''
        writer.writerow([ apellido_paterno, apellido_materno , primer_nombre , segundo_nombre , 
            obj.fecha_nacimiento, obj.get_grado_display(), obj.get_institucion_display(), obj.fundador , obj.get_estado_display(), obj.get_perfil_display() , obj.telefono ])

    return response

def export_csv_cumpleanos_mes(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="listado_cumpleanos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Apellido Paterno', 'Apellido Materno', 'Primer Nombre', 'Segundo Nombre', 'Fecha', 'Grado', 
        'Institucion', 'Fundador','Estado', 'Perfil','Telefono'])

    fecha_actual = datetime.now()
    month = fecha_actual.month
    next_month = fecha_actual.replace(month=month % 12 + 1, day=1)

    sol = Usuario.objects.filter( 
                      fecha_nacimiento__month__in=[month, next_month.month]).order_by('fecha_nacimiento__day')
    

    for obj in sol:
        try:
            apellido_paterno = obj.apellido_paterno.capitalize()
        except AttributeError:
            apellido_paterno = ''

        try:
            apellido_materno = obj.apellido_materno.capitalize()
        except AttributeError:
            apellido_materno = ''

        try:
            primer_nombre = obj.primer_nombre.capitalize()
        except AttributeError:
            primer_nombre = ''

        try:
            segundo_nombre = obj.segundo_nombre.capitalize()
        except AttributeError:
            segundo_nombre = ''

        writer.writerow([ apellido_paterno, apellido_materno , primer_nombre , segundo_nombre , 
            obj.fecha_nacimiento, obj.get_grado_display(), obj.get_institucion_display(), obj.fundador , obj.get_estado_display(), obj.perfil , obj.telefono ])

    return response

def export_csv_listado(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="listado_de Jugadores.csv"'

    writer = csv.writer(response)
    writer.writerow(['Listado','Fecha','Apellido Paterno', 'Apellido Materno', 'Primer Nombre', 'Segundo Nombre',
     'Categoria', 'Indice', 'Carro', 'Acompañante'
       ])

    torneo= request.COOKIES.get('torneoId') 
    current = Torneo.objects.get(id= torneo)

    sol = Solicitud.objects.filter(torneo=current).order_by('fecha')
       
    for indice, obj in enumerate(sol, start=1):
        try:
            apellido_paterno = obj.usuario.apellido_paterno.capitalize()
        except AttributeError:
            apellido_paterno = ''

        try:
            apellido_materno = obj.usuario.apellido_materno.capitalize()
        except AttributeError:
            apellido_materno = ''

        try:
            primer_nombre = obj.usuario.primer_nombre.capitalize()
        except AttributeError:
            primer_nombre = ''

        try:
            segundo_nombre = obj.usuario.segundo_nombre.capitalize()
        except AttributeError:
            segundo_nombre = ''

        writer.writerow([indice, obj.fecha, apellido_paterno, apellido_materno,primer_nombre,segundo_nombre,
                     obj.usuario.get_categoria_display(), obj.indice, obj.carro, obj.acompanantes])
    return response


class salida( CapitanMixin, UpdateView):
    model = Torneo
    form_class = FormularioTorneoUpdateCapitan
    template_name = "capitan/views/salida.html"

    def get_object(self, **kwargs):
        torneoId= self.request.COOKIES.get('torneoId') 
        current = self.model.objects.get(id= torneoId)
        return current 


    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb

        contexto["title"] = "Torneo"
        contexto["titulo"] = "Torneo"

        contexto['btnAction']   = 'ACTUALIZAR'
        contexto['urlForm']     = self.request.path

        front = Paginas_Socio.objects.filter(titulo="salida")
        contexto['front']  = list(front.values('titulo','img', 'contenido','file'))
 
        contexto['rol'] = self.request.user.perfil

        elClubMenu = ElClub.objects.order_by('order')
        contexto['elClub'] = list(elClubMenu.values('archivo', 'titulo'))


        return contexto


    def post(self,request,*args,**kwargs):     # comunicacion entre en form y python para notificaciones
        if request.is_ajax():
            form = self.form_class(request.POST,request.FILES,instance = self.get_object())
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                mensaje = ' Actualizado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido actualizar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('home')




class cumpleanos(CapitanMixin,TemplateView):
    template_name = "capitan/views/cumpleanos.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        dato = Paginas_Socio.objects.get(tipo ="Cump")
        contexto['value']  = dato
        contexto["title"] = dato.tituloPestana
        contexto['rol'] = self.request.user.perfil

        fecha_actual = datetime.now()
        month = fecha_actual.month
        next_month = fecha_actual.replace(month=month % 12 + 1, day=1)

        # Obtener el nombre del mes actual y del próximo utilizando los choices
        nombre_mes_actual = dict(MESES)[month]
        nombre_mes_proximo = dict(MESES)[next_month.month]

        contexto['mes'] = f"{nombre_mes_actual} - {nombre_mes_proximo}"

        # Filtrar los cumpleaños solo para el mes actual y el próximo mes
        listado = Usuario.objects.filter(
            fecha_nacimiento__month__in=[month, next_month.month]
        ).order_by('fecha_nacimiento__day')

        paginator = Paginator(listado, 10)
        page = self.request.GET.get('page')
        contexto['datos'] = paginator.get_page(page)
        return contexto