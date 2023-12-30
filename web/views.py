# from django.shortcuts import render

# Create your views here.

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

from .mixins import *
from .utils import *
from django.shortcuts import HttpResponse
from datetime import datetime
from socios.utils import contact

nameWeb = "CGM"

# Create your views here.
class home(TemplateView, View):
    template_name = "views/home.html"
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
        # Obtener datos del formulario
            nombre = request.POST.get('nombre')
            email = request.POST.get('email')
            asunto = request.POST.get('asunto')
            mensaje = request.POST.get('mensaje')
            tipo = 'formulario_contacto' 
            print(f'enviando formulario_contacto: nombre{nombre}, email:{email}, asunto:{asunto}, mensaje:{mensaje}, tipo:{tipo}')
            contact(tipo, nombre, asunto, mensaje, email)  

        contexto = self.get_context_data()

        return self.render_to_response(contexto)
        #return render(request, 'views/home.html')


    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "home"

        galeria = Galeria.objects.order_by('order')
        federaciones = Links.objects.filter(tipo="F").order_by('order')
        noticias = Links.objects.filter(tipo="NR").order_by('order')
        tours = Links.objects.filter(tipo="TR").order_by('order')
        tiendas = Links.objects.filter(tipo="T").order_by('order')
        reglas = Links.objects.filter(tipo="R").order_by('order')

        # front = Front.objects.filter(titulo="historia")
        
        # print(galeria)

        if len(galeria)==0:
            print('hola')

        contexto['galeria']  = list(galeria.values('titulo','img', 'order'))
        contexto['federaciones']  = list(federaciones.values('titulo','img', 'url'))
        contexto['noticias']  = list(noticias.values('titulo','img', 'url'))
        contexto['tours']  = list(tours.values('titulo','img', 'url'))
        contexto['tiendas']  = list(tiendas.values('titulo','img', 'url'))
        contexto['reglas']  = list(reglas.values('titulo','img', 'url'))
        # contexto['front']  = list(front.values('titulo','img', 'contenido', 'order'))
        # #contexto['personal']  = list(front.values('titulo','img', 'tipo', 'subtitulo', 'order'))

        return contexto

# Create your views here.
class historia(TemplateView):
    template_name = "views/historia.html"
    # template_name = "root/empty.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "historia"
        front = Front.objects.filter(titulo="historia")
        
        listado_p = Listado.objects.filter(tipo__tipo__in=['Presidentes']).filter(actual=False)


        # contexto['front']  = list(front.values('titulo','img', 'contenido', 'order'))[0]
        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        contexto['listado_p'] = list(listado_p.values('titulo', 'img', 'order'))
        contexto['listado_pTitulo'] = 'Antiguos Presidentes'
        # print(contexto['front'] )
        #contexto['personal']  = list(front.values('titulo','img', 'tipo', 'subtitulo', 'order'))

        return contexto

class notFound404(TemplateView):
    template_name = "views/404.html"

    def get_context_data(self,**kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['nameWeb'] = nameWeb
        contexto['title'] = '404'
        front = Front.objects.filter(titulo="404")
        datos = list(front.values('titulo','img', 'contenido'))
        if len(datos ) > 0:
            contexto['front'] =  datos
            contexto['h1']     = datos[0]['contenido']
        else:
            contexto['front'] = []
            contexto['h1']     = 'No hay sitio'
        print('contexto') 
        print(contexto['front'])

        return contexto  

class comite(TemplateView):
    template_name = "views/comite.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "comite"
        
        front = Front.objects.filter(titulo="comite")
        #listado_rc = Listado.objects.filter(tipo__tipo="ComisionRC")
        listado = Listado.objects.filter(tipo__tipo__in=['ComisionRC','ComisionED', 'Responsable Institucional'])

        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        contexto['listado'] = list(listado.values('titulo', 'img', 'tipo__tipo', 'order'))

        return contexto

# Create your views here.
class directorio(TemplateView):
    template_name = "views/directorio.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "directorio"
        front = Front.objects.filter(titulo="directorio")
        listado_m = Listado.objects.filter(tipo__tipo__in=['Directorio'])
        listado_cap = Listado.objects.filter(tipo__tipo__in=['Capitan']).filter(actual=True)
        listado_p = Listado.objects.filter(tipo__tipo__in=['Presidentes']).filter(actual=True)

        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        contexto['listado_m'] = list(listado_m.values('titulo', 'img', 'order', 'tipo__tipo', 'order'))
        contexto['listado_cap'] = list(listado_cap.values('titulo', 'img', 'order', 'tipo__tipo', 'order'))
        contexto['listado_p'] = list(listado_p.values('titulo', 'img', 'order', 'tipo__tipo', 'order'))
        
        contexto['listado_pTitulo'] = 'Presidente Actual'
        contexto['listado_capTitulo'] = 'Capitan Actual'
        return contexto

# Create your views here.
class normas_reglas(TemplateView):
    template_name = "views/normas_reglas.html"
    # template_name = "root/empty.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "normas y reglas"
        front = Front.objects.filter(titulo="normas_reglas")
        
        #listado = Listado.objects.filter(tipo='presidentes')
        listado = NormaRegla.objects.all()

        # contexto['front']  = list(front.values('titulo','img', 'contenido', 'order'))[0]
        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        contexto['listado'] = list(listado.values('titulo', 'descripcion', 'archivo', 'order'))
        # print(contexto['front'] )
        #contexto['personal']  = list(front.values('titulo','img', 'tipo', 'subtitulo', 'order'))

        return contexto

class estatutos(TemplateView):
    template_name = "views/estatutos.html"
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb

        contexto["title"] = "Estatutos"
        front = Front.objects.filter(titulo="Estatutos")
        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        
        return contexto
