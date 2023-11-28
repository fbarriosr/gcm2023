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


nameWeb = "CGM"


# Create your views here.
class home(TemplateView):
    template_name = "views/home.html"
    # template_name = "root/empty.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "home"

        galeria = Galeria.objects.order_by('order')
        link = Links.objects.order_by('order')
        # front = Front.objects.filter(titulo="historia")
        
        # print(galeria)

        if len(galeria)==0:
            print('hola')

        contexto['galeria']  = list(galeria.values('titulo','img', 'order'))
        contexto['link']  = list(link.values('titulo','img', 'parrafo', 'order'))
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

# Create your views here.
class noticia(DetailView):
    model = Noticia
    template_name = "views/noticia.html"
   
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "noticia"
        dato =  self.get_object()
        contexto['new'] =  dato[0]
        dato = list(dato.values('titulo','img','fecha','resumen','info','slug','img1', 'img2', 'img3','img4','img5','region'))
        dato = dato[0]
        lista = []
        if(dato['img1']!=''):
            lista.append(dato['img1'])
        if(dato['img2']!=''):
            lista.append(dato['img2'])
        if(dato['img3']!=''):
            lista.append(dato['img3'])
        if(dato['img4']!=''):
            lista.append(dato['img4'])
        if(dato['img5']!=''):
            lista.append(dato['img5'])

        contexto['imgs']= lista
        contexto['front']= [{'img': dato['img']}]

        return contexto

    def get_object(self, **kwargs):
        print('slug', self.kwargs.get('slug', None))
        slug =  self.model.objects.filter(slug = self.kwargs.get('slug', None))
        return slug

# Create your views here.
class principal_noticias(TemplateView):
    model = Noticia
    template_name = "views/principal_noticias.html"
    
    def get_queryset(self):
        
        lNoticia = self.model.objects.filter(is_active=True).filter(is_aprobado=True).order_by('fecha')
        paginator = Paginator(lNoticia,3)
        page = self.request.GET.get('page')
        lNoticia = paginator.get_page(page)
            
        return lNoticia


    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "noticias"
        contexto['datos'] = self.get_queryset()

        if contexto['datos'].paginator.num_pages > 1 and contexto['datos'].number != contexto['datos'].paginator.num_pages : # tiene un next
            if contexto['datos'].paginator.num_pages - contexto['datos'].next_page_number() > 1:
                contexto['up'] = True     
            else:
                contexto['up'] = False 
        if contexto['datos'].paginator.num_pages > 2 and contexto['datos'].number != 1 : # hay un previo
            if contexto['datos'].previous_page_number()  - 1 > 1:
                contexto['down'] = True     
            else:
                contexto['down'] = False 

        return contexto

class torneos(SocioMixin,TemplateView):
    template_name = "views/torneos.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "torneo"
        mainCard = Torneo.objects.filter(proximo = True)
        #torneoCard = Torneo.objects.filter(activo = True).filter(proximo=False)
        torneoCard = Torneo.objects.filter(proximo=False).order_by('-fecha')
        contexto['mainCard'] = mainCard
        contexto['torneoCard'] = torneoCard
        return contexto



class ranking(TemplateView):
    template_name = "views/ranking.html"
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb

        contexto["title"] = "ranking"
        front = Front.objects.filter(titulo="ranking")
        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        
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
    
# Create your views here.
class cuotas(TemplateView):
    template_name = "views/cuotas.html"
  
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "normas y reglas"

        año_filtro = 2021
        rut_usuario = '16665758-K'
        front = Front.objects.filter(titulo="cuotas")
        #listado = NormaRegla.objects.all()
        listado = Cuota.objects.filter(año__año=año_filtro, usuario__rut=rut_usuario).select_related('año', 'usuario')
        mes_datetime = [datetime(año_filtro, mes, 1) for mes in range(1,13)]

        for cuota in listado:
            cuota.mes_datetime = mes_datetime[cuota.mes -1]

        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        contexto['listado'] = listado
        return contexto
    
# Create your views here.
class torneo_resumen(TemplateView):
    template_name = "views/torneo_resumen.html"
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "torneo_resumen"
        front = Front.objects.filter(titulo="torneo")
        
        listado = NormaRegla.objects.all()

        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        contexto['listado'] = list(listado.values('titulo', 'descripcion', 'archivo', 'order'))

        return contexto
    

# Formulario con las opciones de Cuotas los socios del club.    
def generar_cuotas_form(request):
    return render(request,'views/generar_cuotas_form.html')

#def generar_cuotas(request, año, valor):
def generar_cuotas(request):
    if request.method == 'POST':
        año =   request.POST.get('año')
        valor = request.POST.get('valor')
        respuesta = generar_cuotas_grupal(año, valor)
        return HttpResponse(respuesta)
    return HttpResponse(f'algo anda mal')

def generar_cuotas_socio(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        año = request.POST.get('año')
        respuesta = generar_cuotas_individual(rut, año)
        return HttpResponse(respuesta)
    return HttpResponse(f'algo anda mal')
    #return render(request,'views/generar_cuotas_form.html')

def borrar_cuotas(request):
    if request.method == 'POST':
        año = request.POST.get('año')
        respuesta = borrar_cuotas_grupal(año)
        return HttpResponse(respuesta)
    return HttpResponse(f'Algo anda mal')

def borrar_cuotas_socio(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        año = request.POST.get('año')
        respuesta = borrar_cuotas_individual(rut, año)
        return HttpResponse(respuesta)
    return HttpResponse(f'algo anda mal')
    #return render(request,'views/generar_cuotas_form.html')