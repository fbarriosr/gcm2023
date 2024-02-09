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

from .utils import *
from django.shortcuts import HttpResponse
from datetime import datetime
from socios.utils import contact
from .forms import FormHome
from django.http import JsonResponse


nameWeb = "CGM"

# Create your views here.
class home(TemplateView, View):  
    template_name = "web/views/home.html"
    
    def post(self, request, *args, **kwargs):
        form = FormHome(request.POST)
        
        if form.is_valid():
            print('formulario válido')
            print(form.cleaned_data['captcha'])

            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            asunto = form.cleaned_data['asunto']
            mensaje = form.cleaned_data['mensaje']
            tipo = 'formulario_contacto'

            contact(tipo, nombre, asunto, mensaje, email)

            return redirect("home")

        # Si el formulario no es válido, rellenar con datos proporcionados por el usuario
        form.initial = {
            'nombre': request.POST.get('nombre', ''),
            'email': request.POST.get('email', ''),
            'asunto': request.POST.get('asunto', ''),
            'mensaje': request.POST.get('mensaje', ''),
            # Agrega otros campos según sea necesario
        }

        contexto = {'form': form}
        return render(request, 'web/views/home.html', contexto)



    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "home"

        galeria = Galeria.objects.order_by('order')
        banner = Links.objects.filter(banner=True).order_by('order')
        linksMenu = Links.objects.filter(banner=False).order_by('tipo','order')
        
        contexto['galeria']  = list(galeria.values('titulo','img', 'order'))
        contexto['banner'] = list(banner)
        contexto['linksMenu'] = list(linksMenu.values('url', 'titulo'))
        # contexto['form'] = FormHome()
        
        # Recuperar los datos del formulario de la sesión si existen
        form_data = self.request.session.pop('form_data', {})
        contexto['form'] = FormHome(initial=form_data)   

        return contexto

# Create your views here.
class historia(TemplateView):
    template_name = "web/views/historia.html"
    # template_name = "root/empty.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "historia"
        front = Front.objects.filter(titulo="historia")
        
        listado_p = Listado.objects.filter(tipo__tipo__in=['Presidente']).filter(actual=False)


        # contexto['front']  = list(front.values('titulo','img', 'contenido', 'order'))[0]
        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        contexto['listado_p'] = list(listado_p.values('titulo', 'img', 'order'))
        contexto['listado_pTitulo'] = 'Antiguos Presidentes'
        
        linksMenu = Links.objects.filter(banner=False).order_by('tipo','order')
        contexto['linksMenu'] = list(linksMenu.values('url', 'titulo'))

        return contexto

class notFound404(TemplateView):
    template_name = "web/views/404.html"

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
    template_name = "web/views/comite.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "comite"
        
        front = Front.objects.filter(titulo="comite")
        #listado_rc = Listado.objects.filter(tipo__tipo="ComisionRC")
        listado = Listado.objects.filter(tipo__tipo__in=['ComisionRC','ComisionED', 'Responsable Institucional'])

        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        contexto['listado'] = list(listado.values('titulo', 'img', 'tipo__tipo', 'order'))

        linksMenu = Links.objects.filter(banner=False).order_by('tipo','order')
        contexto['linksMenu'] = list(linksMenu.values('url', 'titulo'))

        return contexto

# Create your views here.
class directorio(TemplateView):
    template_name = "web/views/directorio.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "directorio"
        front = Front.objects.filter(titulo="directorio")
        listado_d = Listado.objects.filter(grupo='D').filter(actual=True)
        listado_m = Listado.objects.filter(grupo='M').filter(actual=True)
       

        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        contexto['listado_m'] = listado_m
        contexto['listado_d'] = listado_d
      
        
        linksMenu = Links.objects.filter(banner=False).order_by('tipo','order')
        contexto['linksMenu'] = list(linksMenu.values('url', 'titulo'))

        return contexto


class estatutos(TemplateView):
    template_name = "web/views/estatutos.html"
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb

        contexto["title"] = "Estatutos"
        front = Front.objects.filter(titulo="estatutos")
        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        
        linksMenu = Links.objects.filter(banner=False).order_by('tipo','order')
        contexto['linksMenu'] = list(linksMenu.values('url', 'titulo'))

        return contexto

def manifest(request):
    data = {
        "name": "Club de Golf Militar",
        "short_name": "CGM",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#fff",
        "description": "Pagina web del club de golf",
        "icons": [{
            "src": "static/web/assets/favicon/favicon-32x32.png",
            "sizes": "32x32",
            "type": "image/png"
        }, {
            "src": "static/web/assets/favicon/favicon-32x32.png",
            "sizes": "32x32",
            "type": "image/png"
        }]
    }
    
    return JsonResponse(data)