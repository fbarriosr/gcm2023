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
from django.core.paginator import Paginator

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from django.db.models import Q

from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required

from django.shortcuts import HttpResponse
from datetime import datetime, date
from .mixins import *
from .forms import *
from .utils import *
from .choices import estado_cuota
import json
import logging

logger = logging.getLogger(__name__)

nameWeb = "CGM"


#def generar_cuotas(request, año, valor):
def generar_cuotas(request):
    print('ingresando a generar_cuotas..')
    if request.method == 'POST':
        form = GenerarCuotasForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            respuesta = generar_cuotas_grupal(data['año'], data['valor'], data['descuento'], data['cargo'])
            print('respuesta:', respuesta)
            if respuesta == 'Operacion exitosa':
                messages.success(request, 'Las cuotas del año se generaron con éxito')
                return HttpResponseRedirect(reverse('generar_cuotas_form'))
            else:
                messages.error(request, respuesta)
                return render(request, 'error.html', {'mensaje_error': respuesta}) 
    else:
        form = GenerarCuotasForm()

    print('saliendo de generar_cuotas..')
    return render(request, 'socio/views/generar_cuotas_form.html', {'form': form})

#def generar_cuotas(request, año, valor):
def generar_cuotas2(request):
    print('ingresando a generar_cuotas..')
    if request.method == 'POST':
        form = GenerarCuotasForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            respuesta = generar_cuotas_grupal(data['año'], data['valor'], data['descuento'], data['cargo'])
            print('respuesta:', respuesta)
            if respuesta == 'Operacion exitosa':
                messages.success(request, 'Las cuotas del año se generaron con éxito')
                return HttpResponseRedirect(reverse('generar_cuotas_form'))
            else:
                messages.error(request, respuesta)
                return render(request, 'error.html', {'mensaje_error': respuesta}) 
    else:
        form = GenerarCuotasForm()

    print('saliendo de generar_cuotas..')
    return render(request, 'socio/views/generar_cuotas_form.html', {'form': form})



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

def restablecer_cuotas_socio(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        año = request.POST.get('año')
        respuesta = restablecer_cuotas_individual(rut, año)
        return HttpResponse(respuesta)
    return HttpResponse(f'algo anda mal')

class PasswordUsuario(SocioMixin,UpdateView):
    model = Usuario
    form_class = FormularioUsuarioPassword
    template_name = 'socio/views/password.html'

    def get_context_data(self,**kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['title'] =  "Usuario"
        contexto['btnAction'] = 'Modificar'
        contexto['titulo'] = 'Cambiar Password'
        contexto['name'] = self.request.user.primer_nombre +' ' +self.request.user.apellido_paterno + ' | ' + self.request.user.get_perfil_display()
        contexto['rol'] = self.request.user.perfil
        return contexto
        
    def post(self,request,*args,**kwargs):     # comunicacion entre en form y python para notificaciones
        if request.is_ajax():
            form = self.form_class(request.POST,instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = 'La contraseña se ha actualizado' 
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
            
    def get_object(self, **kwargs):
        current_user =  Usuario.objects.get(rut=self.request.user.rut)
        return current_user
 
class perfil(SocioMixin,UpdateView):

    model = Usuario
    form_class = FormularioPerfilUpdate
    template_name = "socio/views/perfil.html"
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb

        contexto["title"] = "perfil"
        contexto["titulo"] = "perfil"
        contexto['name'] = self.request.user.primer_nombre +' ' +self.request.user.apellido_paterno + ' | ' + self.request.user.get_perfil_display()

        contexto['btnAction']   = 'ACTUALIZAR'
        contexto['urlForm']     = self.request.path

        contexto['rol'] = self.request.user.perfil

        contexto['user']  = self.get_object()
        return contexto

    def get_object(self, **kwargs):
        
        current_user =  Usuario.objects.get(rut=self.request.user.rut)
        return current_user
    def post(self,request,*args,**kwargs):     # comunicacion entre en form y python para notificaciones
        if request.is_ajax():
            form = self.form_class(request.POST,instance = self.get_object())
            if form.is_valid():
                form.save()
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


# Create your views here.
class noticia(SocioMixin,DetailView):
    model = Noticia
    template_name = "socio/views/noticia.html"
   
    def get(self, *args, **kwargs):
        dato =  self.get_object()
        noticiaId = dato[0].id
        response = super().get( *args, **kwargs)
        response.set_cookie('noticiaId', noticiaId )
        return response

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

        contexto['rol'] = self.request.user.perfil

        return contexto

    def get_object(self, **kwargs):
        print('slug', self.kwargs.get('slug', None))
        slug =  self.model.objects.filter(slug = self.kwargs.get('slug', None))
        return slug

# Create your views here.
class noticias(SocioMixin,TemplateView):
    model = Noticia
    template_name = "socio/views/noticias.html"
    
    def get_queryset(self):
        rol = self.request.user.perfil
        if rol =='SECR' or rol =='SUPER':
            lNoticia = self.model.objects.order_by('fecha')
        else:
            lNoticia = self.model.objects.filter(is_active=True).order_by('fecha')
        paginator = Paginator(lNoticia,9)
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

        contexto['rol'] = self.request.user.perfil

        return contexto


class torneos(SocioMixin,TemplateView):
    template_name = "socio/views/torneos.html"

    def get_context_data(self, **kwargs):
        
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "torneo"
        mainCard = Torneo.objects.filter(activo=True).filter(proximo = True)
        torneoCard = Torneo.objects.filter(activo=True).filter(proximo= False).order_by('-fecha')
        
        diccionario_fechas = list(Torneo.objects.filter(activo=True).values('fecha'))

        if len(diccionario_fechas) > 0:

            # Obtener los años de cada fecha en una lista
            anios = [elemento['fecha'].year for elemento in diccionario_fechas]

            # Encontrar el año mínimo y máximo en la lista de años
            anio_minimo = min(anios)
            anio_maximo = max(anios)

            if anio_maximo != anio_minimo:
                contexto['year'] = str(anio_minimo) +'-'+ str(anio_maximo)
            else:
            	contexto['year'] = str(anio_minimo)
        
        else:
            contexto['year'] = 'SIN FECHAS'

        contexto['mainCard'] = mainCard
        contexto['torneoCard'] = torneoCard
        
        contexto['rol'] = self.request.user.perfil

        return contexto

    def get(self, *args, **kwargs):
        response = super().get( *args, **kwargs)
        response.delete_cookie('torneoId')
        return response

# Create your views here.
class torneo(SocioMixin,DetailView):
    model = Torneo
    template_name = "socio/views/torneo.html"
    
    def get(self, *args, **kwargs):
        dato =  self.get_object()
        torneoId = dato.id
        torneoEstado = dato.abierto
        solicitud = Solicitud.objects.filter(usuario__email=self.request.user.email).filter(torneo__id=torneoId).order_by('-fecha')
        
        if (torneoEstado==True): #torneo abierto

            if (len(solicitud)==0 ): # solicitud
                response = redirect('solicitud') # para inscribir
                response.set_cookie('torneoId', torneoId)
                return response
            else:
                if(solicitud[0].estado =='S'): #arrependido
                    response = redirect('solicitud') # para inscribir
                    response.set_cookie('torneoId', torneoId)
                    return response 
                else: 
                    response = super().get( *args, **kwargs)
                    response.set_cookie('torneoId', torneoId)
                    return response  
        else: 
            response = super().get( *args, **kwargs)
            response.set_cookie('torneoId', torneoId)
            return response
        
       
    def get_context_data(self, **kwargs):

        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        dato =  self.get_object()
        torneoid = dato.id
        torneoEstado = dato.abierto
        contexto['torneoEstado'] = torneoEstado
        contexto['torneoImg']= dato.img
        contexto['torneoFecha']= str(dato.fecha)
        contexto['torneoLugar']= dato.direccion+'-' + dato.region
        contexto['torneoInscritos']= dato.inscritos
        contexto['torneoCupos']= dato.cupos
        solicitud = Solicitud.objects.filter(usuario__email=self.request.user.email).filter(torneo__id=torneoid).order_by('-fecha') #ultima solicitud
        contexto['rol'] = self.request.user.perfil

        if (len(solicitud)==0 ): # no hay solicitud
            if (torneoEstado==False): #torneo Cerrado
                contexto['solicitudEstado']= 'C'
                contexto['nombreTorneo'] = dato.titulo
        else:  # si hay solictud
            contexto['solicitud']= solicitud[0]
            contexto['solicitudEstado']=solicitud[0].estado
            if (solicitud[0].estado == 'A'):
                contexto['bases']= solicitud[0].torneo.bases
                contexto['premiacion']= solicitud[0].torneo.premiacion
                contexto['resultados']= solicitud[0].torneo.resultados
                contexto['listadoAceptados'] = dato.list_inscritos
            elif (solicitud[0].estado == 'S'):
                if (torneoEstado==False): #torneo Cerrado
                    contexto['solicitudEstado']= 'C'
                    contexto['nombreTorneo'] = dato.titulo

        return contexto

    

    def get_object(self, **kwargs):
        torneo_id = self.request.COOKIES.get('torneoId')

        if torneo_id:
            current = Torneo.objects.get(id= torneo_id)
        else:
            print(self.kwargs.get('slug', None))
            current =  Torneo.objects.get(slug = self.kwargs.get('slug', None))

        return current


class crearSolicitud(SocioMixin,CreateView):
    model = Solicitud
    form_class = FormularioSolicitudView
    template_name = "socio/views/solicitud.html"

    def get_form(self, form_class=None):

        deuda_socio = 3
        recargo = 5000
        cuota = 7500

        form = super().get_form(form_class)

        form.fields['deuda_socio'].initial = deuda_socio
        form.fields['recargo'].initial = recargo
        form.fields['cuota'].initial = cuota

        return form
    
    def get_context_data(self,**kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['nameWeb']     =  nameWeb
        
        contexto['btnAction']   = 'Enviar'
        contexto['urlForm']     = self.request.path

        torneo   = self.get_object()
        contexto['torneo'] = torneo
        torneoTitulo = str(torneo.titulo).upper().replace('TORNEO','') 
        contexto['titulo'] = 'INSCRIPCIÓN  TORNEO '+ torneoTitulo
        contexto['rol'] = self.request.user.perfil
     
        return contexto

    def get_object(self, **kwargs):
        torneo= self.request.COOKIES.get('torneoId') 
        current = Torneo.objects.get(id= torneo)
        return current 

    def post(self,request,*args,**kwargs):  
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                solicitud = Solicitud(
                    usuario      = Usuario.objects.get(rut=  self.request.user.rut),
                    torneo       = self.get_object(), 
                    fecha        = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    auto = form.cleaned_data.get('auto'),
                    patente = form.cleaned_data.get('patente'),
                    busCGM = form.cleaned_data.get('busCGM'),
                    carro =  form.cleaned_data.get('carro'),
                    indice       = form.cleaned_data.get('indice'),
                    acompanantes = self.request.POST.get('acompanantes'),
                    descripcion  = form.cleaned_data.get('descripcion'),
                    deuda_socio  = form.cleaned_data.get('deuda_socio'),
                    cancela_deuda_socio = form.cleaned_data.get('cancela_deuda_socio'),
                    recargo      = form.cleaned_data.get('recargo'),
                    cuota        = form.cleaned_data.get('cuota'),
                    monto        = form.cleaned_data.get('monto'),
                    
                )
                
                solicitud.save()
                mensaje = 'Solicitud Enviada'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                print('errorAqui')
                mensaje = 'not pe'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('home')


class crearSolicitudSuspender(SocioMixin,CreateView):
    model = Solicitud
    form_class = FormularioSolicitudSuspenderCreate
    template_name = "socio/views/suspender.html"

    def get_context_data(self,**kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['nameWeb']     =  nameWeb
        
        contexto['btnAction']   = 'Enviar'
        contexto['urlForm']     = self.request.path

        torneo   = self.get_object()
        contexto['torneo'] = torneo
        torneoTitulo = str(torneo.titulo).upper().replace('TORNEO','') 
        contexto['titulo'] = 'SOLICITUD DE SUSPENCION PARTICIPACIÓN '+ torneoTitulo
        contexto['rol'] = self.request.user.perfil
     
        return contexto

    def get_object(self, **kwargs):
        torneo= self.request.COOKIES.get('torneo') 
        current = Torneo.objects.get(id= torneo)
        return current 

    def get_solicitud(self, **kwargs):
        torneo   = self.get_object()
        torneoid = torneo.id
        current = Solicitud.objects.filter(usuario__rut=self.request.user.rut).filter(torneo__id=torneoid).filter(estado='A').order_by('-fecha')
        return current


    def post(self,request,*args,**kwargs):  
        if request.is_ajax():
            solicitud = self.get_solicitud()[0]
            form = self.form_class(request.POST)
            if form.is_valid():
                solicitud = Solicitud(
                    usuario      = Usuario.objects.get(rut=  solicitud.rut),
                    torneo       = self.get_object(), 
                    fecha        = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    auto         = solicitud.auto,
                    patente      = solicitud.patente,
                    busCGM       = solicitud.busCGM,
                    carro        = solicitud.carro,
                    indice       = solicitud.indice,
                    acompanantes = solicitud.acompanantes,
                    descripcion  = solicitud.descripcion,
                    deuda_socio  = solicitud.deuda_socio,
                    cancela_deuda_socio = solicitud.cancela_deuda_socio,
                    recargo      = solicitud.recargo,
                    cuota        = solicitud.cuota,
                    monto        = solicitud.monto,
                    suspende     = True,
                    motivoSuspencion =  form.cleaned_data.get('motivoSuspencion')
                )
                solicitud.save()
                mensaje = 'Solicitud Enviada'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                print('errorAqui')
                mensaje = 'not pe'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('home')

class ranking(SocioMixin,TemplateView):
    template_name = "socio/views/ranking.html"
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb

        contexto["title"] = "ranking"
        front = Front.objects.filter(titulo="ranking")
        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        contexto['rol'] = self.request.user.perfil
        
        return contexto
    def get(self, *args, **kwargs):
        rankingId = Front.objects.filter(titulo="ranking")
        response = super().get( *args, **kwargs)
        response.set_cookie('rankingId', rankingId[0].id)
        return response


# LA ESTRUCTURA DE LAS CUOTAS DE LOS SOCIOS DEL CLUB CGM

class cuotas_admin(SocioMixin,TemplateView, View):
    
    ''' Vista para la administración de cuotas de los Secretarios
        ---------------------------------------------------------
        desde esta vista se aprueban o rechazan las cuotas en estado
        de 'En Revision', enviadas por los socios del club. 
    '''
    
    template_name = "socio/views/cuotas_admin.html"

    def get_queryset(self):

        buscar = self.request.GET.get('buscar')
        print(f'print buscar = {buscar}') 
        logger.info(f'logger buscar = {buscar}') 

        try:
            front = Front.objects.filter(titulo="cuotas")  

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

            return {
                'cuotas': cuotas,
                'front': list(front.values('titulo','img', 'contenido', 'order','file')),
                'años_cuotas_socio': años_cuotas_socio,
                'listado_usuarios': listado_usuarios,
                'rol': self.request.user.perfil
            }

        
        except Exception as e:
            print(f"Error al obtener datos del contexto: {str(e)}")
            
            cuotas = []
            front = []
            años_cuotas_socio = []
            listado_usuarios = []

            # Imprimir detalles del error
            import traceback
            print(traceback.format_exc())

            return {
                'cuotas': cuotas,
                'front': front,
                'años_cuotas_socio': años_cuotas_socio,
                'listado_usuarios': listado_usuarios,
                'rol': self.request.user.perfil  # o el valor que prefieras en caso de error
            }

    def get_context_data(self, **kwargs):
    
        # contexto =  super().get_context_data(**kwargs)
        datos = self.get_queryset()

        cuotas = datos['cuotas']
        front = datos['front']
        años_cuotas_socio = datos['años_cuotas_socio']
        listado_usuarios = datos['listado_usuarios']

        contexto = {
            'nameWeb': nameWeb,
            'front': front,
            'title': 'cuotas_admin_mod',
            'rol': self.request.user.perfil,
            'datos': cuotas,
            'cuotas': cuotas,
            'años_cuotas_socio': años_cuotas_socio,
            'listado_usuarios': listado_usuarios,
        }
        
        return contexto

    def post(self, request, *args, **kwargs):

        # Verificar que se haya ejecutado el metodo POST antes de procesar
        if request.method == 'POST': 
            
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
                        cuotas_a_actualizar.append(Cuota(id=cuota_id, estado_pago=mapeo_estados[estado_cuota]))
                try:
                    # Actualizamos el estado de la cuota en la bd.
                    Cuota.objects.bulk_update(cuotas_a_actualizar, fields=['estado_pago'])    
                except Exception as e:
                    print(f"Error al actualizar las cuotas: {str(e)}")
                
            return redirect("cuotas_admin") 


#@login_required Si se usa con request, sin heredar de vistas
@method_decorator(login_required, name='dispatch')
class cuotas(SocioMixin,TemplateView, View):
    template_name = "socio/views/cuotas.html"

    def get(self, request, *args, **kwargs):
        
        # Indicador de descuento de cuotas por promocion
        mostrar_promocion = False
        
        # Obtener el año y mes actual
        año_actual = datetime.now().year
        mes_actual = datetime.now().month
        rut = self.request.user.rut

        # Verificar si el usuario tiene cuotas para el año actual
        cuotas_usuario = Cuota.objects.filter(usuario=request.user, año__año=año_actual)
    
        # Obtener el rango de duracion (inicio y fin) de la promoción del presente año.
        if cuotas_usuario.exists():
            duracion_descuento = cuotas_usuario.first().año

            # Obtenemos True si el mes actual esta en el rango de duracion del descuento
            if duracion_descuento:
                meses_descuento = list(range(duracion_descuento.periodo_des_inicio, duracion_descuento.periodo_des_fin + 1))
                mostrar_promocion = mes_actual in meses_descuento

        # Establecer los QuerySet de front y Cuotas
        front = Front.objects.filter(titulo="cuotas")
        cuotas = Cuota.objects.filter(usuario__rut=rut).select_related('usuario')

        # Crear una lista de objetos datetime para representar los meses del año
        mes_cuota = [datetime(2000, mes, 1) for mes in range(1, 13)]

        # Añadir el campo 'mes_datetime' a cada instancia de Cuota
        for cuota in cuotas:
            cuota.mes_cuota = mes_cuota[cuota.mes - 1]

        print(f"valor del descuento: {duracion_descuento.descuento}") 
        # Crear el contexto de la vista con los datos a renderizar
        contexto = {
            "nameWeb": nameWeb,
            "title": "cuotas",
            "front": list(front.values('titulo', 'img', 'contenido', 'order','file')),
            "cuotas": cuotas,
            "mostrar_promocion": mostrar_promocion,
            "descuento_anual": duracion_descuento.descuento,
            "rol": self.request.user.perfil
        }

        return self.render_to_response(contexto)

    def post(self, request, *args, **kwargs):
        try:
            # Verificar que se haya ejecutado el metodo POST antes de procesar
            if request.method != 'POST':
                raise ValueError("Invalid request method")
            
            estado_revision = next((code for code, value in estado_cuota if value == 'En Revision'), None)

            # Establecer las variables necesarias que vienen del formulario
            data_str = request.POST.get('data', '[]')
            cuotasSeleccionadas = json.loads(data_str)

            # Comprobamos la informacion y actualizamos el estado de las cuotas de 'Pendiente' a 'En Revision'
            if not cuotasSeleccionadas:
                raise ValueError("No se encontraron cuotas seleccionadas")

            cuota_ids = [cuota.get('id_cuota') for cuota in cuotasSeleccionadas]
            filas_afectadas = Cuota.objects.filter(id__in=cuota_ids).update(estado_pago=estado_revision)

            # Si se aplicó la actualizacion, obtenemos los datos a enviar por correo
            if filas_afectadas < 1:
                raise ValueError("No se realizaron actualizaciones, compruebe los datos datos del formulario.")

            tipo='pago_cuota' if filas_afectadas == 1 else 'pago_cuotas'  
            email=cuotasSeleccionadas[0]['email']
            mes=int(cuotasSeleccionadas[0]['mes'])
            año=int(cuotasSeleccionadas[0]['año'])
            
            if 'descuento' in cuotasSeleccionadas[0]:
                descuento_str   = cuotasSeleccionadas[0]['descuento']
                print(f'descuento activo?:{descuento_str}')

                # Verificamos si se debe aplicar un descuento a las cuotas antes de enviar el correo
                if descuento_str is None:
                    descuento = None
                else:
                    try:
                        descuento = int(descuento_str)
                    except ValueError as e:
                        # print('Error: el descuento no es un valor numérico o válido. Detalles: {e}') 
                        descuento = 0
            else:
                descuento = None
                print('Error: la variable descuento no esta en el diccionario') 

            # Sumamos el monto total de las cuotas a pagar y enviamos el correo.
            total_pagar = sum(int(cuota.get('monto_cuota')) for cuota in cuotasSeleccionadas)
            resultado = contact(tipo, email=email, total_pagar=total_pagar, mes=mes, año=año, descuento=descuento)
            
            # Establecer un mensaje de aviso al volver a la plantilla html
            messages.success(request, resultado)

            return redirect('cuotas')
        
        except ValueError as ve:
            print(f"Error en el proceso principal: {str(ve)}")

        except json.JSONDecodeError as jde:
            print(f"Error al decodificar JSON: {str(jde)}")
            messages.error(request, "Ocurrió un error al decodificar JSON.")

        except Exception as e:
            print(f"Error en el proceso principal: {str(e)}")
            messages.error(request, "Ocurrió un error en el proceso principal.")

        return redirect('cuotas')