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
from django.db.models import Q, Sum
from django.shortcuts import HttpResponse
from datetime import datetime
from web.models import *
from socios.models import *
from socios.mixins import *
import csv
from django.core.paginator import Paginator
from socios.forms import *
from .forms import *

nameWeb = "CGM"


class solicitudHome(TesoreroMixin, TemplateView):
    template_name = "tesorero/views/solicitudesHome.html"
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb

        contexto["title"] = "Solicitudes"
        contexto['rol'] = self.request.user.perfil

        torneoId = self.request.COOKIES.get('torneoId') 
        pendientes 	= Solicitud.objects.filter(torneo__id=torneoId).filter(estado='P')
        aprobadas 	= Solicitud.objects.filter(torneo__id=torneoId).filter(estado='A')
        rechazadas 	= Solicitud.objects.filter(torneo__id=torneoId).filter(estado='R')
        suspendidos = Solicitud.objects.filter(torneo__id=torneoId).filter(estado='S')

        contexto['pendientes']  = len(pendientes)
        contexto['aprobadas']  	= len(aprobadas)
        contexto['rechazadas']  = len(rechazadas)
        contexto['suspendidas'] = len(suspendidos)
    

        return contexto


class listarSolicitudes(TesoreroMixin, View):
    model = Solicitud
    form_class = FormularioSolicitudView
    template_name = "tesorero/views/solicitudesListar.html"

    def get_queryset(self):
        
        buscar = self.request.GET.get('buscar')
        estado = self.request.GET.get('estado')
        torneoid = self.request.COOKIES.get('torneoId')

        lSolicitudes = self.model.objects.filter(torneo__id=torneoid)

        if estado in ['P', 'A', 'S', 'R']:
            lSolicitudes = lSolicitudes.filter(estado=estado)

        if buscar:
            if buscar.upper() in ['TODO', 'TODOS', '*']:
                lSolicitudes = lSolicitudes.order_by('fecha')
            else:
                lSolicitudes = lSolicitudes.filter(
                    Q(usuario__rut__icontains=buscar) |
                    Q(usuario__apellido_paterno__icontains=buscar) |
                    Q(usuario__primer_nombre__icontains=buscar)
                ).distinct()
        else:
            lSolicitudes = lSolicitudes.order_by('fecha')

        
        paginator = Paginator(lSolicitudes,8)
        page = self.request.GET.get('page')
        lSolicitudes = paginator.get_page(page)   
        return lSolicitudes
    
    def get_context_data(self,**kwargs):
        contexto = {}

        contexto['title']       = 'Solicitudes'
        contexto['nameWeb']     =  'Listado de Solicitudes'
        contexto['subtitle']    =  'Listado de Solicitudes'
         
        estado = self.request.GET.get('estado')
        if estado:
            contexto['estado']      =  estado
        else:
             contexto['estado']      = ''
       
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




class solicitudUpdate(TesoreroMixin,UpdateView):
    model = Solicitud
    form_class = FormularioSolicitudUpdateTesorero
    template_name = "tesorero/views/solicitudUpdate.html"

    def get_object(self, **kwargs):
        noticiaId= self.request.COOKIES.get('solicitudId') 
        current = self.model.objects.get(id= noticiaId)
        return current

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb

        contexto["title"] = "Solicitud"
        contexto["titulo"] = 'Solicitud'
        torneoId = self.get_object().torneo.id

        contexto['user'] = Usuario.objects.get(id= self.request.user.id)
        contexto['torneo'] = Torneo.objects.get(id= torneoId )

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


class resumenCuotas(TesoreroMixin, TemplateView):

    ''' Vista para la administración de socios
        ---------------------------------------------------------
        desde esta vista se visualiza el resumen del estado de pagos de los socios, 
        como van durante el año y si se encuentran al día, o por el contrario arrastran
        alguna deuda pendiente. 
    '''

    template_name = "tesorero/views/resumenCuotas.html"
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "Resumen Cuotas"
        contexto['rol'] = self.request.user.perfil

        def calcular_monto_total(cuotas):
            return cuotas.aggregate(Sum('año__monto_cuota'))['año__monto_cuota__sum'] or 0

        # Obtener el año actual
        año_actual = int(datetime.now().year)   

        # Obtener la lista de usuarios unicos con cuota en el año actual
        lista_usuarios = Usuario.objects.all()
        print(f"cantidad usuarios: {len(lista_usuarios)}")

        # Lista que almacenara los datos relacionados con las cuotas para cada usuario
        resumen_usuarios = []

        # Obtenemos localmente las cuotas para evitar consultas a la bd por cada calculo
        cuotas_anuales = Cuota.objects.all()

        # Resumen de cuotas por usuario
        for usuario in lista_usuarios:
            
            # Calculos de cuotas para el año en curso
            cuotas_año_actual = cuotas_anuales.filter(año__año=año_actual, usuario=usuario)

            cuotas_pagadas = cuotas_año_actual.filter(estado_pago='A',).count()
            cuotas_impagas = cuotas_año_actual.filter(~Q(estado_pago='A'),).count()
            monto_pagado = calcular_monto_total(cuotas_año_actual.filter(estado_pago = 'A'))
            monto_impago = calcular_monto_total(cuotas_año_actual.filter(~Q(estado_pago='A')))

            # Calculos relacionados con cuotas de años anteriores
            cuotas_años_anteriores = cuotas_anuales.exclude(año__año=año_actual).filter(usuario=usuario)

            deuda_pendente= calcular_monto_total(cuotas_años_anteriores.filter(~Q(estado_pago='A')))
            deuda_total = deuda_pendente + monto_impago

            resumen_usuario = {
                "nombre": f"{usuario.primer_nombre} {usuario.apellido_paterno}",
                "es_activo": 'si' if usuario.is_active else 'no',
                "rut": usuario.rut,
                "deuda_pendiente": deuda_pendente,
                "cuotas_pagadas": cuotas_pagadas,
                "monto_pagado": monto_pagado,
                "cuotas_impagas": cuotas_impagas,
                "monto_impago": monto_impago,
                "al_dia": 'si' if Cuota.objects.filter(estado_pago='A', año__año=año_actual).count() == 12 else 'no',
                "deuda_total": deuda_total,
                "pendiente": 'si' if deuda_total > 0 else 'no'
            }

            resumen_usuarios.append(resumen_usuario)

        contexto["resumen_usuarios"] = resumen_usuarios
        contexto["año_actual"] = año_actual

        return contexto
