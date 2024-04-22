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
from django.http import HttpResponseNotFound


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
        else:
            # Si el formulario no es válido, aún así incluir los elementos en el contexto
            contexto = self.get_context_data(form=form, error_message="Por favor verifica la activacion del captcha")
            return render(request, 'web/views/home.html', contexto)



    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "Bienvenidos al club"

        galeria = Galeria.objects.order_by('order')
        banner = Links.objects.filter(banner=True).order_by('order')
        linksMenu = Links.objects.filter(banner=False).order_by('tipo','order')
        
        contexto['galeria']  = list(galeria.values('titulo','img', 'order'))
        contexto['banner'] = list(banner)
        contexto['linksMenu'] = list(linksMenu.values('url', 'titulo'))
        # contexto['form'] = FormHome()
        
        # Recuperar los datos del formulario de la sesión si existen
        form_data = self.request.session.pop('form_data', {})
        # Incluye el formulario en el contexto sin inicialización especial
        contexto['form'] = kwargs.get('form', FormHome())
        contexto['error_message'] = kwargs.get('error_message', None)

        return contexto
    

# Create your views here.
class historia(TemplateView):
    template_name = "web/views/historia.html"
    # template_name = "root/empty.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        
        dato = Paginas_Web.objects.get(tipo ="H")
        contexto['value']  = dato
        contexto["title"] = dato.tituloPestana
        linksMenu = Links.objects.filter(banner=False).order_by('tipo','order')
        contexto['linksMenu'] = list(linksMenu.values('url', 'titulo'))

        return contexto

class NotFound404(TemplateView):
    template_name = "web/views/404.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        
        dato = Paginas_Web.objects.get(tipo ="404")
        contexto['value']  = dato
        contexto["title"] = dato.tituloPestana
        linksMenu = Links.objects.filter(banner=False).order_by('tipo','order')
        contexto['linksMenu'] = list(linksMenu.values('url', 'titulo'))
        return contexto


def handler404(request, exception):
    return HttpResponseNotFound(NotFound404.as_view()(request=request).content)

class comite(TemplateView):
    template_name = "web/views/comite.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        
        
        dato = Paginas_Web.objects.get(tipo ="C")
        contexto['value']  = dato
        contexto["title"] = dato.tituloPestana

       
        listado = Listado.objects.filter(tipo__tipo__in=['ComisionRC','ComisionED', 'Responsable Institucional'])

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
        

        dato = Paginas_Web.objects.get(tipo ="D")
        contexto['value']  = dato
        contexto["title"] = dato.tituloPestana
    
        listado_d = Listado.objects.filter(grupo='D').filter(actual=True)
        listado_m = Listado.objects.filter(grupo='M').filter(actual=True)
   

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
        
        dato = Paginas_Web.objects.get(tipo ="E")
        contexto['value']  = dato
        contexto["title"] = dato.tituloPestana
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