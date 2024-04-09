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
from django.db.models import Q
from web.models import *
from usuarios.models import *
from socios.models import *
from socios.mixins import *
import csv
from django.core.paginator import Paginator
from .forms import *


nameWeb = "CGM"

def export_csv_bus( request):
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
        contexto['rol'] = self.request.user.perfil
        front = Front.objects.filter(titulo="bus")
        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        torneoid = self.request.COOKIES.get('torneo') 
        listado = Solicitud.objects.filter(torneo__id=torneoid).filter(estado = 'A').filter(busCGM= True).order_by('usuario__apellido_paterno')
        paginator = Paginator(listado,1)
        page = self.request.GET.get('page')
        contexto['datos']= paginator.get_page(page)

        return contexto

class rankingUpdate(SecretarioMixin,UpdateView):
    model = Front
    form_class = FormularioRankingUpdate
    template_name = "secretario/views/rankingUpdate.html"

    def get_object(self, **kwargs):
        rankingId= self.request.COOKIES.get('rankingId') 
        current = Front.objects.get(id= rankingId)
        return current 

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb

        contexto["title"] = "ranking"
        contexto["titulo"] = "ranking"

        contexto['btnAction']   = 'ACTUALIZAR'
        contexto['urlForm']     = self.request.path

        contexto['rol'] = self.request.user.perfil

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


class auto(SecretarioMixin, TemplateView):
    template_name = "secretario/views/auto.html"
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb

        contexto["title"] = "AUTO"
        front = Front.objects.filter(titulo="auto")
        contexto['rol'] = self.request.user.perfil
        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        torneoid = self.request.COOKIES.get('torneo') 
        listado = Solicitud.objects.filter(torneo__id=torneoid).filter(estado = 'A').filter(auto= True).order_by('usuario__apellido_paterno')
        paginator = Paginator(listado,1)
        page = self.request.GET.get('page')
        contexto['datos']= paginator.get_page(page)
        return contexto

class noticiaUpdate(SecretarioMixin,UpdateView):
    model = Noticia
    form_class = FormularioNoticiaUpdate
    template_name = "secretario/views/noticiaUpdate.html"

    def get_object(self, **kwargs):
        noticiaId= self.request.COOKIES.get('noticiaId') 
        current = self.model.objects.get(id= noticiaId)
        return current 


    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb

        contexto["title"] = "noticia"
        contexto["titulo"] = "noticia"

        contexto['btnAction']   = 'ACTUALIZAR'
        contexto['urlForm']     = self.request.path

        contexto['rol'] = self.request.user.perfil

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

        
class noticiaCreate(SecretarioMixin,CreateView):
    model = Noticia
    form_class = FormularioNoticiaCreate
    template_name = "secretario/views/noticiaCreate.html"
    
    def get_context_data(self,**kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['nameWeb']     =  nameWeb
        
        contexto['btnAction']   = 'Enviar'
        contexto['urlForm']     = self.request.path

        contexto['titulo'] = 'CREAR NOTICIA'
        contexto['rol'] = self.request.user.perfil
     
        return contexto


    def post(self,request,*args,**kwargs):  
        if request.is_ajax():
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                noticia = Noticia(
                    titulo      = form.cleaned_data.get('titulo'),
                    fecha       = form.cleaned_data.get('fecha'),
                    direccion   = form.cleaned_data.get('direccion'),
                    region      = form.cleaned_data.get('region'),
                    resumen     = form.cleaned_data.get('resumen'),
                    info        = form.cleaned_data.get('info'),
                    img         = form.cleaned_data.get('img'),
                    img1        = form.cleaned_data.get('img1'),
                    img2        = form.cleaned_data.get('img2'),
                    img3        = form.cleaned_data.get('img3'),
                    img4        = form.cleaned_data.get('img4'),     
                )
                noticia.save()
                mensaje = 'Noticia Enviada'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                print('errorAqui')
                mensaje = 'Error'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('home')

class noticiaDelete(SecretarioMixin,DeleteView):
    model = Noticia
    template_name = "secretario/views/noticiaDelete.html"
    def delete(self,request,*args,**kwargs):
        if request.is_ajax():
            noticia = self.get_object()
            noticia.delete()
            mensaje = f'{self.model.__name__} eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('noticias')
    def get_object(self, **kwargs):
        noticiaId= self.request.COOKIES.get('noticiaId') 
        noticia = self.model.objects.get(id=noticiaId)
        return noticia

class torneoCreate(SecretarioMixin,CreateView):
    model = Torneo
    form_class = FormularioTorneoCreate
    template_name = "secretario/views/torneoCreate.html"
    
    def get_context_data(self,**kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['nameWeb']     =  nameWeb
        
        contexto['btnAction']   = 'Crear'
        contexto['urlForm']     = self.request.path

        contexto['titulo'] = 'CREAR TORNEO'
        contexto['rol'] = self.request.user.perfil
     
        return contexto


    def post(self,request,*args,**kwargs):  
        if request.is_ajax():
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                torneo = Torneo(
                    titulo            = form.cleaned_data.get('titulo'),
                    fecha             = form.cleaned_data.get('fecha'),
                    direccion         = form.cleaned_data.get('direccion'),
                    region            = form.cleaned_data.get('region'),
                    descripcion       = form.cleaned_data.get('descripcion'),
                    cupos             = form.cleaned_data.get('cupos'),
                    inscritos         = form.cleaned_data.get('inscritos'),
                    activo            = form.cleaned_data.get('activo'),
                    proximo           = form.cleaned_data.get('proximo'),
                    abierto           = form.cleaned_data.get('abierto'),
                    bases             = form.cleaned_data.get('bases'),
                    list_inscritos    = form.cleaned_data.get('list_inscritos'),
                    list_salidas      = form.cleaned_data.get('list_salidas'),
                    resultados        = form.cleaned_data.get('resultados'),
                    premiacion        = form.cleaned_data.get('premiacion'),
                )
                torneo.save()
                mensaje = 'Torneo Enviado'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                print('errorAqui')
                mensaje = 'Error'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('home')



class torneoUpdate(SecretarioMixin,UpdateView):
    model = Torneo
    form_class = FormularioTorneoUpdate
    template_name = "secretario/views/torneoUpdate.html"

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

        contexto['rol'] = self.request.user.perfil

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



class torneoDelete(SecretarioMixin,DeleteView):
    model = Torneo
    template_name = "secretario/views/torneoDelete.html"
    def delete(self,request,*args,**kwargs):
        if request.is_ajax():
            torneo = self.get_object()
            torneo.delete()
            mensaje = f'{self.model.__name__} eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('torneos')
    def get_object(self, **kwargs):
        torneoId= self.request.COOKIES.get('torneoId') 
        torneo = self.model.objects.get(id=torneoId)
        return torneo

class listarUsuarios(SecretarioMixin, View):
    model = Usuario
    form_class = FormularioUsuariosView
    template_name = "secretario/views/listarUsuarios.html"

    def get_queryset(self):
        
        buscar = self.request.GET.get('buscar')
        print(f'listar usuarios buscar: {buscar}') 
        if buscar:  
            if buscar.upper() in ['TODO', 'TODOS', '*']:
                    lUsuarios = self.model.objects.order_by('apellido_paterno')
            else:
                lUsuarios = self.model.objects.filter(
                    Q(rut__icontains=buscar) |
                    Q(apellido_paterno__icontains=buscar) |
                    Q(primer_nombre__icontains=buscar)
                ).distinct()
        else:
            lUsuarios = self.model.objects.order_by('apellido_paterno')
        
        paginator = Paginator(lUsuarios,8)
        page = self.request.GET.get('page')
        lUsuarios = paginator.get_page(page)   
        return lUsuarios
    
    def get_context_data(self,**kwargs):
        contexto = {}

        contexto['title']       = 'Usuarios'
        contexto['nameWeb']     =  'Usuarios'
        contexto['subtitle']    =  'Listado de Usuarios'
         
        contexto['msmEmpty']    =  'No hay resultados'
        
        contexto['form']      = self.form_class
        contexto['datos']     = self.get_queryset()

        contexto['rol'] = self.request.user.perfil

        
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
      
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,self.get_context_data())





class usuarioUpdate(SecretarioMixin,UpdateView):
    model = Usuario
    form_class = FormularioUsuariosView
    template_name = "secretario/views/usuarioUpdate.html"

    def get_object(self, **kwargs):
        usuarioId= self.request.COOKIES.get('usuarioId') 
        current = self.model.objects.get(id= usuarioId)
        return current 

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb

        contexto["title"] = "Usuario"
        contexto["titulo"] = "Usuario"

        contexto['btnAction']   = 'ACTUALIZAR'
        contexto['urlForm']     = self.request.path

        contexto['rol'] = self.request.user.perfil

        return contexto


    def post(self,request,*args,**kwargs):     # comunicacion entre en form y python para notificaciones
        if request.is_ajax():
            form = self.form_class(request.POST,instance = self.get_object())
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

class usuarioCreate(SecretarioMixin,CreateView):
    model = Usuario
    form_class = FormularioUsuariosView
    template_name = "secretario/views/usuarioCreate.html"
    
    def get_context_data(self,**kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['nameWeb']     =  nameWeb
        
        contexto['btnAction']   = 'Enviar'
        contexto['urlForm']     = self.request.path

        contexto['titulo'] = 'CREAR USUARIO'
        contexto['rol'] = self.request.user.perfil
     
        return contexto


    def post(self,request,*args,**kwargs):  
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                usuario = Usuario(
                    rut                 = form.cleaned_data.get('rut'),
                    primer_nombre       = form.cleaned_data.get('primer_nombre'),
                    segundo_nombre       = form.cleaned_data.get('segundo_nombre'),
                    apellido_paterno    = form.cleaned_data.get('apellido_paterno'),
                    apellido_materno    = form.cleaned_data.get('apellido_materno'),
                    email               = form.cleaned_data.get('email'),
                    telefono            = form.cleaned_data.get('telefono'),
                    fecha_nacimiento    = form.cleaned_data.get('fecha_nacimiento'),
                    estado              = form.cleaned_data.get('estado'),
                    categoria           = form.cleaned_data.get('categoria'),
                    sexo                = form.cleaned_data.get('sexo'),
                    eCivil              = form.cleaned_data.get('eCivil'),
                    perfil              = form.cleaned_data.get('perfil'),
                    situacionEspecial   = form.cleaned_data.get('situacionEspecial'),
                    fundador            = form.cleaned_data.get('fundador'),
                    is_admin            = form.cleaned_data.get('is_admin'),
                    is_active           = form.cleaned_data.get('is_active'),
                    institucion         = form.cleaned_data.get('institucion'),
                    grado               = form.cleaned_data.get('grado'),
                    profesion           = form.cleaned_data.get('profesion'),
                    condicion           = form.cleaned_data.get('condicion'),
                    fecha_incorporacion = form.cleaned_data.get('fecha_incorporacion'),
                )
                usuario.set_password(form.cleaned_data.get('rut'))
                usuario.save()
                mensaje = 'Usuario Creado'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                print('errorAqui')
                mensaje = 'Error'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('home')

