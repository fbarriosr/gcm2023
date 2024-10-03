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
from secretario.forms import FormularioUsuariosView
from datetime import datetime, date
import logging
import json

nameWeb = "CGM"

logger = logging.getLogger(__name__)



def export_csv_solicitudes(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="solicitudesListar.csv"'

    writer = csv.writer(response)
    writer.writerow(['Fecha','Rut','Apellido Paterno', 'Primer Nombre', 
        'Deudas', 'Recargo Socio', 'Recargo Invitado','Cuota', 'Cancela Deuda socio (NO/SI)','TIcket Bus','Cancela Bus (NO/SI)','TOTAL', 'Detalle CUOTAS PAGADAS'])

    buscar = request.GET.get('buscar')
    estado = request.GET.get('estado')
    torneoid = request.COOKIES.get('torneoId')

    lSolicitudes = Solicitud.objects.filter(torneo__id=torneoid)

    if buscar:
        buscar_upper = buscar.upper()
        if buscar_upper in ['TODO', 'TODOS', '*']:
            lSolicitudes = lSolicitudes.order_by('fecha')
        else:
            lSolicitudes = lSolicitudes.filter(
                Q(usuario__rut__icontains=buscar_upper) |
                Q(usuario__apellido_paterno__icontains=buscar_upper) |
                Q(usuario__primer_nombre__icontains=buscar_upper)
            ).distinct()
    else:
        lSolicitudes = lSolicitudes.order_by('fecha')

    for obj in lSolicitudes:
        try:
            apellido_paterno = obj.usuario.apellido_paterno.capitalize()
        except AttributeError:
            apellido_paterno = ''

        try:
            primer_nombre = obj.usuario.primer_nombre.capitalize()
        except AttributeError:
            primer_nombre = ''

        writer.writerow([ obj.fecha,obj.usuario.rut,apellido_paterno, primer_nombre , 
             obj.deuda_socio, obj.recargo,obj.recargo_invitado ,obj.cuota , obj.cancela_deuda_socio, obj.recargo_bus, obj.busCGM  ,obj.monto, obj.detalle_cuotas_pagadas])

    return response




def export_csv_resumen_cuotas(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="resumen_cuotas.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nombre', 'RUT', 'Deuda Pendiente', 'Cuotas Pagadas', 'Monto Pagado', 'Cuotas Impagas', 'Monto Impago', 'Al Día', 'Deuda Total', 'Pendiente'])

    # Crear una instancia de la clase resumenCuotas y pasarle el request
    vista_resumen_cuotas = resumenCuotas()
    resumen_cuotas = vista_resumen_cuotas.get_queryset(request=request)  # Pasar el request aquí

    for usuario in resumen_cuotas:
        writer.writerow([
            usuario['nombre'],
            usuario['rut'],
            usuario['deuda_pendiente'],
            usuario['cuotas_pagadas'],
            usuario['monto_pagado'],
            usuario['cuotas_impagas'],
            usuario['monto_impago'],
            usuario['al_dia'],
            usuario['deuda_total'],
            usuario['pendiente']
        ])

    return response









class resumenCuotas(TesoreroMixin, TemplateView):

    ''' Vista para la administración de socios
        ---------------------------------------------------------
        desde esta vista se visualiza el resumen del estado de pagos de los socios, 
        como van durante el año y si se encuentran al día, o por el contrario arrastran
        alguna deuda pendiente. 
    '''
    model = Usuario
    form_class = FormularioUsuariosView
    template_name = "tesorero/views/resumenCuotas.html"

    def get_front(self):
        return Paginas_Socio.objects.get(tipo="C")
    
    def calcular_monto_total(self, cuotas):
        return cuotas.aggregate(Sum('año__monto_cuota'))['año__monto_cuota__sum'] or 0

    def get_queryset(self, request=None):
        if request is None:
            request = self.request

        buscar = request.GET.get('buscar')
        año_actual = int(datetime.now().year)

        # Obtener la lista de usuarios únicos con cuota en el año actual
        lista_usuarios = Usuario.objects.all().order_by('apellido_paterno')
        if buscar:
            lista_usuarios = lista_usuarios.filter(
                Q(rut__icontains=buscar) |
                Q(apellido_paterno__icontains=buscar) |
                Q(primer_nombre__icontains=buscar)
            ).distinct()

        # Obtener todas las cuotas para el año actual y años anteriores
        cuotas_anuales = Cuota.objects.select_related('año').filter(año__año=año_actual)
        cuotas_años_anteriores = Cuota.objects.select_related('año').exclude(año__año=año_actual)

        # Obtener todas las cuotas para cada usuario
        cuotas_por_usuario = {}
        for usuario in lista_usuarios:
            cuotas_por_usuario[usuario.pk] = {
                'año_actual': cuotas_anuales.filter(usuario=usuario),
                'años_anteriores': cuotas_años_anteriores.filter(usuario=usuario)
            }

        resumen_usuarios = []
        for usuario in lista_usuarios:
            cuotas_usuario = cuotas_por_usuario[usuario.pk]

            cuotas_año_actual_usuario = cuotas_usuario['año_actual']
            cuotas_años_anteriores_usuario = cuotas_usuario['años_anteriores']

            cuotas_pagadas = cuotas_año_actual_usuario.filter(estado_pago='A').count()
            cuotas_impagas = cuotas_año_actual_usuario.exclude(estado_pago='A').count()
            monto_pagado = self.calcular_monto_total(cuotas_año_actual_usuario.filter(estado_pago='A'))
            monto_impago = self.calcular_monto_total(cuotas_año_actual_usuario.exclude(estado_pago='A'))

            deuda_pendiente = self.calcular_monto_total(cuotas_años_anteriores_usuario.exclude(estado_pago='A'))
            deuda_total = deuda_pendiente + monto_impago

            resumen_usuario = {
                "nombre": f"{usuario.primer_nombre} {usuario.apellido_paterno}",
                "es_activo": 'si' if usuario.is_active else 'no',
                "rut": usuario.rut,
                "deuda_pendiente": deuda_pendiente,
                "cuotas_pagadas": cuotas_pagadas,
                "monto_pagado": monto_pagado,
                "cuotas_impagas": cuotas_impagas,
                "monto_impago": monto_impago,
                "al_dia": 'si' if cuotas_año_actual_usuario.count() == 12 else 'no',
                "deuda_total": deuda_total,
                "pendiente": 'si' if deuda_total > 0 else 'no'
            }

            resumen_usuarios.append(resumen_usuario)

        return resumen_usuarios

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['value'] = self.get_front()
        contexto['nameWeb'] = nameWeb
        contexto["title"] = "Resumen Cuotas"
        contexto['rol'] = self.request.user.perfil
        contexto['datos'] = self.get_queryset()
        contexto["resumen_usuarios"] = self.get_queryset()
        
        return contexto

   
# LA ESTRUCTURA DE LAS CUOTAS DE LOS SOCIOS DEL CLUB CGM

class cuotas_admin(SecretarioMixin,TemplateView, View):

    ''' Vista para la administración de cuotas de los Secretarios
        ---------------------------------------------------------
        desde esta vista se aprueban o rechazan las cuotas en estado
        de 'En Revision', enviadas por los socios del club.
    '''

    template_name = "tesorero/views/cuotas_admin.html"

    def get_queryset(self):

        buscar = self.request.GET.get('buscar')
        # print(f'print buscar = {buscar}')
        logger.info(f'logger buscar = {buscar}')

        try:
            front = Paginas_Socio.objects.get(tipo ="C")
            if buscar:
                if  buscar.upper() in ['TODO', 'TODOS', '*']:
                    cuotas = Cuota.objects.filter(estado_pago='E').select_related('usuario', 'año')
                else:
                    cuotas = Cuota.objects.filter(
                        Q(usuario__rut__icontains=buscar) |
                        Q(usuario__apellido_paterno__icontains=buscar) |
                        Q(usuario__primer_nombre__icontains=buscar)
                    ).filter(Q(estado_pago='E')).select_related('usuario', 'año').distinct()


            else:
                cuotas = Cuota.objects.filter(estado_pago='E').select_related('usuario', 'año')
            # Crear una lista de objetos datetime para representar los meses del año
            mes_cuota = [date(2000, mes, 1) for mes in range(1, 13)]

            # Añadir el campo 'mes_datetime' a cada instancia de Cuota
            for cuota in cuotas:
                cuota.mes_cuota = mes_cuota[cuota.mes - 1]

            # Obtener los años pertenecientes a las cuotas para el filtro de la plantilla.
            años_cuotas_socio = Cuota.objects.values('año__año').distinct().order_by('año__año')
            años_cuotas_socio = sorted([año['año__año'] for año in años_cuotas_socio], reverse=True)

            # Incluir el valor del estado del socio, reemplazando la letra por el nombre
            estado_dict = dict(estado)

            for cuota in cuotas:
                if cuota.usuario.estado in estado_dict:
                    cuota.usuario.estado_txt = estado_dict[cuota.usuario.estado]

            # Obtener la lista de socios para el filtro de la plantilla
            usuarios_con_cuotas = Usuario.objects.filter(cuota__isnull=False).distinct()
            listado_usuarios = usuarios_con_cuotas.values_list('email', flat=True).order_by('-email')

            print(f"cuotas:{len(cuotas)}")   
            for cuota in cuotas:
                print(f"cuota:{cuota}")     

            return {
                'cuotas': cuotas,
                'value': front,
                'años_cuotas_socio': años_cuotas_socio,
                'listado_usuarios': listado_usuarios,
                'rol': self.request.user.perfil
            }

        except Exception as e:
            print(f"Error al obtener datos del contexto: {str(e)}")

            cuotas = []
            value = []
            años_cuotas_socio = []
            listado_usuarios = []

            # Imprimir detalles del error
            import traceback
            print(traceback.format_exc())

            return {
                'cuotas': cuotas,
                'value': value,
                'años_cuotas_socio': años_cuotas_socio,
                'listado_usuarios': listado_usuarios,
                'rol': self.request.user.perfil  # o el valor que prefieras en caso de error
            }

    def get_context_data(self, **kwargs):

        # contexto =  super().get_context_data(**kwargs)
        datos = self.get_queryset()

        cuotas = datos['cuotas']
        value = datos['value']
        años_cuotas_socio = datos['años_cuotas_socio']
        listado_usuarios = datos['listado_usuarios']

        contexto = {
            'nameWeb': nameWeb,
            'value': value,
            'title': 'cuotas_admin_mod',
            'rol': self.request.user.perfil,
            'datos': cuotas,
            'cuotas': cuotas,
            'años_cuotas_socio': años_cuotas_socio,
            'listado_usuarios': listado_usuarios,
        }

        return contexto

    def post(self, request, *args, **kwargs):
        
        # Establecer las variables necesarias que vienen del formulario
        data_str = request.POST.get('data', '[]')
        cuotasSeleccionadas = json.loads(data_str)

        # Comprobamos la informacion y actualizamos el estado de las cuotas de 'Pendiente' a 'En Revision'
        if cuotasSeleccionadas:
            # Comprobamos el estado de las cuotas y las actualizamos en la bd
            mapeo_estados = {'Aprobada': 'A', 'Rechazada': 'R'}
            cuotas_a_actualizar = []

            for cuota in cuotasSeleccionadas:
                cuota_id = cuota.get('id_cuota', None)
                estado_cuota = cuota.get('estado_cuota', None)


                if estado_cuota and estado_cuota in mapeo_estados:
                    cuotas_a_actualizar.append(Cuota(id=cuota_id, estado_pago=mapeo_estados[estado_cuota], fecha_pago= datetime.now().date()))
            try:
                # Actualizamos el estado de la cuota en la bd.
                Cuota.objects.bulk_update(cuotas_a_actualizar, fields=['estado_pago'])
            except Exception as e:
                print(f"Error al actualizar las cuotas: {str(e)}")

        return redirect("cuotas_admin")
