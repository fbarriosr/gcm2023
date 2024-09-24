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
from dateutil.relativedelta import relativedelta
from .mixins import *
from .forms import *
from .utils import *
from .choices import estado_cuota

from itertools import chain
from transbank.webpay.webpay_plus.transaction import Transaction
import logging, random, json, requests , csv

logger = logging.getLogger(__name__)

nameWeb = "CGM"

# Plantilla con formulario para facilitar las operaciones masivas de las cuotas de usuarios
class OperacionesCuotasView(View):

    form = GenerarCuotasForm()

    def get(self, request, *args, **kwargs):
        print('GET request')  

        return render(request, 'socio/views/operaciones_cuotas.html', {'form': self.form})

    def post(self, request, *args, **kwargs):
        print('POST request')

        form = None
        action = request.POST.get('action')

        if action == 'generar_cuotas_anuales_socios':
            form = GenerarCuotasForm(request.POST)
        elif action == 'borrar_cuotas_anuales_socios':
            OperacionesCuotasForm.base_fields['rut'].required = False
            form = OperacionesCuotasForm(request.POST)
        else:
            OperacionesCuotasForm.base_fields['rut'].required = True
            form = OperacionesCuotasForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            if action == 'generar_cuotas_anuales_socios':
                es_valido, respuesta = generar_cuotas_grupal(data['año'], data['valor'], data['descuento'], data['cargo'])
            elif action == 'restablecer_cuotas_anuales_socio':
                es_valido, respuesta = restablecer_cuotas_individual(data['rut'], data['año'])
            elif action == 'generar_cuotas_anuales_nuevo_socio':
                es_valido, respuesta = generar_cuotas_individual(data['rut'], data['año'])
            elif action == 'borrar_cuotas_anuales_socios':
                es_valido, respuesta = borrar_cuotas_grupal(data['año'])
            elif action == 'borrar_cuotas_anuales_socio':
                es_valido, respuesta = borrar_cuotas_individual(data['rut'], data['año'])

            if es_valido:
                messages.success(request, respuesta)
            else:
                messages.error(request, respuesta)

            # Redirigir al usuario a la misma página (GET)
            return redirect('operaciones_cuotas')

        return render(request, 'socio/views/operaciones_cuotas.html', {'form': form})

def export_csv_solicitudesAprobadas(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="solicitudesListarAprobados.csv"'

    writer = csv.writer(response)
    writer.writerow(['Fecha','Rut','Apellido Paterno', 'Primer Nombre',  'INDICE'])

   
    torneoid = request.COOKIES.get('torneoId')

    lSolicitudes = Solicitud.objects.filter(torneo__id=torneoid).order_by('fecha')

    for obj in lSolicitudes:
        try:
            apellido_paterno = obj.usuario.apellido_paterno.capitalize()
        except AttributeError:
            apellido_paterno = ''

        try:
            primer_nombre = obj.usuario.primer_nombre.capitalize()
        except AttributeError:
            primer_nombre = ''

        writer.writerow([ obj.fecha,obj.usuario.rut,apellido_paterno, primer_nombre ,  obj.indice])

    return response


class PasswordUsuario(AutentificadoMixin,UpdateView):
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
        elClubMenu = ElClub.objects.order_by('order')
        contexto['elClub'] = list(elClubMenu.values('archivo', 'titulo'))

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
 
class perfil(AutentificadoMixin,UpdateView):

    model = Usuario
    form_class = FormularioPerfilUpdate
    template_name = "socio/views/perfil.html"
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb

        

        contexto["title"] = 'PERFIL'

        contexto['name'] = self.request.user.primer_nombre +' ' +self.request.user.apellido_paterno + ' | ' + self.request.user.get_perfil_display()

        contexto['btnAction']   = 'ACTUALIZAR'
        contexto['urlForm']     = self.request.path

        contexto['rol'] = self.request.user.perfil

        contexto['user']  = self.get_object()

        elClubMenu = ElClub.objects.order_by('order')
        contexto['elClub'] = list(elClubMenu.values('archivo', 'titulo'))

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
class noticia(AutentificadoMixin,DetailView):
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
        contexto["title"] = "Noticia"
        dato =  self.get_object()
        contexto['new'] =  dato[0]
        
        lista = []

        lista = list(NoticiaImg.objects.filter(noticia = dato[0].id ))
        
        dato = list(dato.values('titulo','img','fecha','resumen','info','slug','region'))
        dato = dato[0]

        contexto['value'] = dato
        contexto['imgs']= lista
        

        contexto['rol'] = self.request.user.perfil

        elClubMenu = ElClub.objects.order_by('order')
        contexto['elClub'] = list(elClubMenu.values('archivo', 'titulo'))

        return contexto

    def get_object(self, **kwargs):
        print('slug', self.kwargs.get('slug', None))
        slug =  self.model.objects.filter(slug = self.kwargs.get('slug', None))
        return slug

# Create your views here.
class noticias(AutentificadoMixin,TemplateView):
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
        
        dato = Paginas_Socio.objects.get(tipo ="Noti")
        contexto['value']  = dato
        contexto["title"] = dato.tituloPestana

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

        elClubMenu = ElClub.objects.order_by('order')
        contexto['elClub'] = list(elClubMenu.values('archivo', 'titulo'))

        return contexto


# Create your views here.
class multimedia(AutentificadoMixin,DetailView):
    model = Multimedia
    template_name = "socio/views/multimedia.html"
   
    def get(self, *args, **kwargs):
        dato =  self.get_object()
        multimediaId = dato[0].id
        response = super().get( *args, **kwargs)
        response.set_cookie('multimediaId', multimediaId )
        return response

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "Multimedia"
        dato =  self.get_object()
        contexto['new'] =  dato[0]
        
        lista = []

        lista = list(MultimediaImg.objects.filter(multimedia = dato[0].id ))
        
        dato = list(dato.values('titulo','img','fecha','slug'))
        dato = dato[0]

        contexto['value'] = dato
        contexto['imgs']= lista
       

        contexto['rol'] = self.request.user.perfil

        elClubMenu = ElClub.objects.order_by('order')
        contexto['elClub'] = list(elClubMenu.values('archivo', 'titulo'))

        return contexto

    def get_object(self, **kwargs):
        print('slug', self.kwargs.get('slug', None))
        slug =  self.model.objects.filter(slug = self.kwargs.get('slug', None))
        return slug

# Create your views here.
class multimedias(AutentificadoMixin,TemplateView):
    model = Multimedia
    template_name = "socio/views/multimedias.html"
    
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
        
        dato = Paginas_Socio.objects.get(tipo ="Multi")
        contexto['value']  = dato
        contexto["title"] = dato.tituloPestana

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

        elClubMenu = ElClub.objects.order_by('order')
        contexto['elClub'] = list(elClubMenu.values('archivo', 'titulo'))

        return contexto



class inicio(AutentificadoMixin,TemplateView):
    template_name = "socio/views/inicio.html"

    def get_context_data(self, **kwargs):
        
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "Inicio"
                     
        galeria = Galeria.objects.order_by('order')
        contexto['galeria']  = list(galeria.values('titulo','img', 'order'))

        torneoCardMain = Torneo.objects.filter(activo=True).filter(actual = True).order_by('-fecha')[:1]  
        actualImg =   CardsInicio.objects.filter(tipo='A')[:1]
    
        # Convertir los querysets a listas si es necesario
        torneoCardMain = list(torneoCardMain)
        actualImg = list(actualImg)

        if (len(torneoCardMain)>0):

            # Iterar simultáneamente sobre torneoCard y proxImg usando zip
            for torneo, img in zip(torneoCardMain, actualImg):
                torneo.img = img.img

            contexto['torneoCardMain'] = torneoCardMain

            torneoCard = Torneo.objects.filter(activo=True,  actual=False, fecha__gt=torneoCardMain[0].fecha).order_by('fecha')[:2]

        else:

            fecha_actual = timezone.now()
                
            torneoCard = Torneo.objects.filter(activo=True, abierto= True, actual=False, fecha__gt=fecha_actual).order_by('fecha')[:2]

        if (len(torneoCard)>0):
            if (len(torneoCard) == 2):
                proxImg = CardsInicio.objects.filter(tipo='P')[:2]
            if (len(torneoCard) == 1):
                proxImg = CardsInicio.objects.filter(tipo='P')[:1]
            
            # Convertir los querysets a listas si es necesario
        
            torneoCard = list(torneoCard)
            proxImg = list(proxImg)

            # Iterar simultáneamente sobre torneoCard y proxImg usando zip
            for torneo, img in zip(torneoCard, proxImg):
                torneo.img = img.img


            contexto['torneoCard'] = torneoCard

        lNoticia = Noticia.objects.filter(is_active=True).order_by('-fecha')[:3]
        contexto['datos'] = lNoticia

        lClub= ElClub.objects.all().order_by('order')[:3]
        contexto['datosClub'] = lClub


        contexto['rol'] = self.request.user.perfil

        elClubMenu = ElClub.objects.order_by('order')
        contexto['elClub'] = list(elClubMenu.values('archivo', 'titulo'))
        return contexto

    def get(self, *args, **kwargs):
        response = super().get( *args, **kwargs)
        response.delete_cookie('torneoId')
        return response


class torneos(AutentificadoMixin,TemplateView):
    template_name = "socio/views/torneos.html"

    def get_context_data(self, **kwargs):
        
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "calendario"

        contexto['rol'] = self.request.user.perfil
      

        if contexto['rol'] == 'SUPER' or contexto['rol'] == 'SECR' :
            torneos = Torneo.objects.all().order_by('-fecha')
        else:
            torneos = Torneo.objects.filter(activo=True).order_by('-fecha')
        
        
        paginator = Paginator(torneos,8)
        page = self.request.GET.get('page')
        torneos = paginator.get_page(page)




        contexto['datos'] = torneos

        dato = Paginas_Socio.objects.get(tipo ="CALEN")

        contexto['value']  = dato
        contexto["title"] = dato.tituloPestana

        

        front = Paginas_Socio.objects.filter(titulo="calendario")
        contexto['front']  = list(front.values('titulo','img', 'contenido','file'))
        

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


        elClubMenu = ElClub.objects.order_by('order')
        contexto['elClub'] = list(elClubMenu.values('archivo', 'titulo'))

        return contexto

    def get(self, *args, **kwargs):
        response = super().get( *args, **kwargs)
        response.delete_cookie('torneoId')
        return response


class crearSolicitud(AutentificadoMixin,CreateView):
    model = Solicitud
    form_class = FormularioSolicitudView
    template_name = "socio/views/solicitud.html"

    def get_form(self, form_class=None):

        
        fecha_actual = datetime.now()

        fecha_cuotas = fecha_actual - relativedelta(months=2)  # es la actual -2 meses


        deuda_socio_anos_anteriores = Cuota.objects.filter(usuario__rut= self.request.user.rut).filter(año__año__lt= fecha_cuotas.year).filter(estado_pago='P').order_by('año__año').order_by('numero_cuota')

        deuda_socia_ano_actual = Cuota.objects.filter(usuario__rut= self.request.user.rut).filter(año__año = fecha_cuotas.year).filter(numero_cuota__lte=fecha_cuotas.month).filter(estado_pago='P').order_by('numero_cuota')

        total_lista = list(deuda_socio_anos_anteriores) + list(deuda_socia_ano_actual) 

        total = 0

        ano_valor = list(CuotaAnual.objects.all())

        if self.request.user.perfil == 'I':
            cuota = self.get_object().ticket
            recargoInvitado =  self.get_object().ticket_inv 
            form = super().get_form(form_class)
            form.fields['detalle_cuotas_pagadas'].initial = []
            form.fields['deuda_socio'].initial = 0
            form.fields['recargo'].initial = 0
            form.fields['recargo_invitado'].initial = recargoInvitado
            form.fields['cuota'].initial = cuota

        elif self.request.user.perfil == 'I_E':
            cuota = 0
            form = super().get_form(form_class)
            form.fields['detalle_cuotas_pagadas'].initial = []
            form.fields['deuda_socio'].initial = 0
            form.fields['recargo'].initial = 0
            form.fields['recargo_invitado'].initial = 0
            form.fields['cuota'].initial = 0

        elif self.request.user.perfil == 'S_E':
            cuota = self.get_object().ticket
            form = super().get_form(form_class)
            form.fields['detalle_cuotas_pagadas'].initial = []
            form.fields['deuda_socio'].initial = 0
            form.fields['recargo'].initial = 0
            form.fields['recargo_invitado'].initial = 0
            form.fields['cuota'].initial = cuota

        elif self.request.user.perfil == 'S_V':
            cuota = self.get_object().ticket
            form = super().get_form(form_class)
            form.fields['detalle_cuotas_pagadas'].initial = []
            form.fields['deuda_socio'].initial = 0
            form.fields['recargo'].initial = 0
            form.fields['recargo_invitado'].initial = 0
            form.fields['cuota'].initial = cuota

        else:

            for t in total_lista:
                for j in ano_valor:
                    if t.año.año== j.año:
                        total = total + j.monto_cuota


            deuda_socio = total

            recargo = self.get_object().recargo
            cuota = self.get_object().ticket

            form = super().get_form(form_class)

            tuplas = [(t.año.año, t.numero_cuota ) for t in total_lista]

            form.fields['detalle_cuotas_pagadas'].initial = tuplas
            form.fields['deuda_socio'].initial = deuda_socio
            form.fields['recargo'].initial = recargo
            form.fields['recargo_invitado'].initial = 0
            form.fields['cuota'].initial = cuota


        return form
    
    def get(self, *args, **kwargs):
        request = self.request
        token = request.GET.get("token_ws")

        # Si hubo una transaccion, procesa su respuesta y actualiza la DB.
        if token:
            print('token detectado')  
            respuestaTransaccion = (Transaction()).commit(token=token)
        
            status = respuestaTransaccion['status']

            if  status == 'AUTHORIZED':
                # Almacena los datos del token y la respuesta de la transacción en la sesión
                request.session['token'] = token
                request.session['respuestaTransaccion'] = respuestaTransaccion
                if request.session['cancela_deuda_socio'] == True:
                    solicitud = Solicitud(
                        usuario      = Usuario.objects.get(rut=  self.request.user.rut),
                        torneo       = self.get_object(), 
                        fecha        = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        auto         = request.session['auto'], 
                        patente      = request.session['patente'],
                        busCGM       = request.session['busCGM'],
                        carro        = request.session['carro'],
                        indice       = request.session['indice'],
                        acompanantes = request.session['acompanantes'],
                        deuda_socio  = request.session['deuda_socio'],
                        cancela_deuda_socio = request.session['cancela_deuda_socio'],
                        recargo      = request.session['recargo'],
                        recargo_invitado      = request.session['recargo_invitado'],
                        cuota        = request.session['cuota'],
                        monto        = request.session['monto'],
                        detalle_cuotas_pagadas  = request.session['detalle_cuotas_pagadas'],
                    )
                        
                    solicitud.save()

                
                    tupla = tuple(eval(request.session['detalle_cuotas_pagadas']))
                    for t in tupla:
                        obj = Cuota.objects.get(usuario__rut = self.request.user.rut, numero_cuota = t[1], año__año=t[0])
                        obj.estado_pago = 'A'
                        obj.save()
                else:
                    solicitud = Solicitud(
                        usuario      = Usuario.objects.get(rut=  self.request.user.rut),
                        torneo       = self.get_object(), 
                        fecha        = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        auto         = request.session['auto'], 
                        patente      = request.session['patente'],
                        busCGM       = request.session['busCGM'],
                        carro        = request.session['carro'],
                        indice       = request.session['indice'],
                        acompanantes = request.session['acompanantes'],
                        deuda_socio  = request.session['deuda_socio'],
                        cancela_deuda_socio = request.session['cancela_deuda_socio'],
                        recargo      = request.session['recargo'],
                        recargo_invitado      = request.session['recargo_invitado'],
                        cuota        = request.session['cuota'],
                        monto        = request.session['monto'],
                    )
                        
                    solicitud.save()


                response = redirect('solicitud') # para inscribir
                return response
            elif status =='FAILED':
                response = redirect(reverse('solicitud') + '?rechazopago=true')
                return response

        else: 
            response = super().get( *args, **kwargs)
            return response 
        

    def get_context_data(self,**kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['nameWeb']     =  nameWeb
        
        contexto['btnAction']   = 'Enviar'
        contexto['urlForm']     = self.request.path

        torneo   = self.get_object()
        contexto['torneo'] = torneo

        if torneo:
            torneoTitulo = str(torneo.titulo).upper().replace('TORNEO','') 
            contexto['titulo'] = 'INSCRIPCIÓN  TORNEO '+ torneoTitulo

            if self.request.GET.get("rechazopago")=="true":
                contexto['subtitulo'] = '¡PAGO RECHAZADO VUELVA A INTENTAR!'
            
                
            contexto['rol'] = self.request.user.perfil
         
            elClubMenu = ElClub.objects.order_by('order')
            contexto['elClub'] = list(elClubMenu.values('archivo', 'titulo'))

            solicitud = Solicitud.objects.filter(usuario__email=self.request.user.email).filter(torneo=torneo).order_by('-fecha')

            if (len(solicitud)> 0 ):
                contexto['pagado']= True

                contexto['mensaje'] = f"""
                Estimado {self.request.user.primer_nombre.capitalize()} {self.request.user.apellido_paterno.capitalize()}<br><br>
                Nos complace informarte que tu inscripción al torneo de golf ha sido pagada con éxito. <br><br>
                ¡Bienvenido al evento!
                <br><br>
                Atentamente <br><br>
                <strong>El Capitan</strong>
                <br><br>

                Nota: <br>Las fotos del Torneo se pueden enviar al email secretario@golfmilitar.cl
                """

            else:
                contexto['pagado']= False
               
                if torneo.region  =='XIII':
                    contexto['local']= True
                else:
                    contexto['local']= False  

            


        return contexto

    def get_object(self, **kwargs):
        torneo= self.request.COOKIES.get('torneoId') 
        current = Torneo.objects.get(id= torneo)
        return current

    def post(self,request,*args,**kwargs):  
        
        form = self.form_class(request.POST)

        if form.is_valid():
           
            busCGM       = form.cleaned_data.get('busCGM'),
            auto         = form.cleaned_data.get('auto'),
            patente      = form.cleaned_data.get('patente'),
            carro        = form.cleaned_data.get('carro'),
            acompanantes = form.cleaned_data.get('acompanantes'),
            indice       = form.cleaned_data.get('indice'),
            
            deuda_socio  = form.cleaned_data.get('deuda_socio'),
            cancela_deuda_socio = form.cleaned_data.get('cancela_deuda_socio'),
            recargo      = form.cleaned_data.get('recargo'),
            recargo_invitado      = form.cleaned_data.get('recargo_invitado'),
            cuota        = form.cleaned_data.get('cuota'),
            monto        = form.cleaned_data.get('monto'),
            detalle_cuotas_pagadas = form.cleaned_data.get('detalle_cuotas_pagadas')


            busCGM       = busCGM[0]
            auto         = auto[0]
            patente      = patente[0]
            carro        = carro[0]
            acompanantes = acompanantes[0]
            indice       = indice[0]
            
            deuda_socio  = deuda_socio[0]
            cancela_deuda_socio = cancela_deuda_socio[0]
            recargo      = recargo[0]
            recargo_invitado      = recargo_invitado[0]

            cuota        = cuota[0]
            monto        = monto[0]
            

            buy_order = str(random.randrange(1000000, 99999999))
            session_id = str(random.randrange(1000000, 99999999))
            amount = str(monto)
            return_url = request.build_absolute_uri(reverse('solicitud'))

            create_request, response = crearTransaccion(buy_order, session_id, amount, return_url)


            # Almacenar los datos en la sesion
            request.session['create_request'] = create_request
            request.session['response'] = response

            request.session['busCGM'] = busCGM 
            request.session['auto'] = auto 
            request.session['patente'] = patente 
            request.session['carro'] = carro 
            request.session['acompanantes'] = acompanantes 
            request.session['indice'] = indice 
            request.session['deuda_socio'] = deuda_socio 
            request.session['cancela_deuda_socio'] = cancela_deuda_socio 
            request.session['recargo'] = recargo 
            request.session['recargo_invitado'] = recargo_invitado 
            request.session['cuota'] = cuota 
            request.session['monto'] = monto 
            request.session['detalle_cuotas_pagadas'] = detalle_cuotas_pagadas

            

            # Redirigir a la vista de procesamiento de transacción
            return redirect('procesar_transaccion')
            
            
        else:
            print('errorAqui')
            mensaje = 'Error:'
            error = form.errors
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 400
            return response
      

class inscritos(AutentificadoMixin, TemplateView):
    template_name = "socio/views/inscritos.html"
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto['rol'] = self.request.user.perfil

        dato = Paginas_Socio.objects.get(tipo ="Ins")
        contexto['value']  = dato
        contexto["title"] = dato.tituloPestana

        torneoid = self.request.COOKIES.get('torneoId') 
        listado = Solicitud.objects.filter(torneo__id=torneoid).order_by('usuario__apellido_paterno')
        paginator = Paginator(listado,1)
        page = self.request.GET.get('page')
        contexto['datos']= paginator.get_page(page)

        elClubMenu = ElClub.objects.order_by('order')
        contexto['elClub'] = list(elClubMenu.values('archivo', 'titulo'))


        return contexto      


class ranking(AutentificadoMixin,TemplateView):
    template_name = "socio/views/ranking.html"
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb

        dato = Paginas_Socio.objects.get(tipo ="R")
        contexto['value']  = dato
        contexto["title"] = dato.tituloPestana

        contexto['rol'] = self.request.user.perfil

        elClubMenu = ElClub.objects.order_by('order')
        contexto['elClub'] = list(elClubMenu.values('archivo', 'titulo'))
        
        return contexto
    
def crearTransaccion(buy_order, session_id, amount, return_url):
    create_request = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url
    }

    response = (Transaction()).create(buy_order, session_id, amount, return_url)
    
    return create_request, response


def procesar_transaccion(request):
    # Obtener los datos de la sesión
    response = request.session.get('response')
    # Construir el formulario HTML con los datos necesarios
    form_html = f'''
        <form id="webpayForm" action="{response['url']}" method="POST">
            <input type="hidden" name="token_ws" value="{response['token']}" />
        </form>
        <script>
            document.getElementById("webpayForm").submit();
        </script>
    '''

    # Retornar el formulario HTML como una respuesta HTTP
    return HttpResponse(form_html)


class cuotas(SociosMixin,TemplateView, View):
    template_name = "socio/views/cuotas.html"
    front = Paginas_Socio.objects.get(tipo ="C")
    Paginas_Socio

    @staticmethod
    def obtenerCuotasSocios(request):
        """
        Obtiene las cuotas de los socios para el usuario actual.

        Parameters:
        - request: El objeto de solicitud de Django.

        Returns:
        Una tupla con tres elementos:
        - mostrar_promocion: Un indicador de si se debe mostrar la promoción.
        - duracion_descuento: El objeto Año de duración del descuento.
        - cuotas: Las cuotas del usuario actual.
        """
        # Obtener el año y mes actual
        año_actual = datetime.now().year
        mes_actual = datetime.now().month
        rut = request.user.rut
        # Verificar si el usuario tiene cuotas para el año actual
        cuotas_usuario = Cuota.objects.filter(usuario=request.user, año__año=año_actual)

        # Comprobamos si se aplicara descuento por promocion primeros meses
        mostrar_promocion = False
        duracion_descuento = None
        if cuotas_usuario.exists():
            duracion_descuento = cuotas_usuario.first().año
            if duracion_descuento:
                meses_descuento = list(range(duracion_descuento.periodo_des_inicio, duracion_descuento.periodo_des_fin + 1))
                mostrar_promocion = mes_actual in meses_descuento

        # Se obtienen las cuotas del usuario actual
        cuotas = Cuota.objects.filter(usuario__rut=rut).select_related('usuario')
        mes_cuota = [datetime(2000, mes, 1) for mes in range(1, 13)]
        # Añadir el campo 'mes_datetime' a cada instancia de Cuota
        for cuota in cuotas:
            cuota.mes_cuota = mes_cuota[cuota.mes - 1]

        return mostrar_promocion, duracion_descuento, cuotas

    @staticmethod
    def enviarCorreoAvisoPago(request, cuotasSeleccionadas):
        """
        Envía correos de aviso de pago.

        Parameters:
        - request: El objeto de solicitud de Django.
        - cuotas_seleccionadas: Lista de cuotas seleccionadas para pago.

        Returns:
        None
        """
        # Determinar el tipo de correo según la cantidad de cuotas seleccionadas
        tipo_correo = 'pago_cuota' if len(cuotasSeleccionadas) == 1 else 'pago_cuotas'
        cuota = cuotasSeleccionadas[0]
        email = cuota['email']
        mes = int(cuota['mes'])
        año = int(cuota['año'])

        # Construir el mensaje de correo
        cuotas_a_pagar = {
            "email": email,
            "total_pagar": request.session.get('total_pagar'),
            "mes": mes,
            "año": año,
            "descuento": request.session.get('descuento'),
        }

        # Enviar el correo
        contact(tipo_correo, None, cuotas_a_pagar)

    @staticmethod
    def actualizaEstadoCuotas(request, respuestaTransaccion):
        """
        Actualiza el estado de las cuotas después de una transacción exitosa.

        Parameters:
        - request: El objeto de solicitud de Django.
        - response2: La respuesta de la transacción.

        Returns:
        Un mensaje indicando el resultado de la actualización.
        """
        # Recuperar los datos del formulario original de la sesión
        cuotasSeleccionadas = request.session.get('cuotas_seleccionadas', [])

        # Si la trasaccion fue exitosa, marcamos las cuotas como Aprobadas y enviamos correo de aviso
        if respuestaTransaccion['status'] == 'AUTHORIZED':
            # Obtener el ID de las cuotas seleccionadas
            cuota_ids = [cuota.get('id_cuota') for cuota in cuotasSeleccionadas]
            # Actualiza el estado de las cuotas en la BD
            filas_afectadas = Cuota.objects.filter(id__in=cuota_ids).update(estado_pago='A', fecha_pago=datetime.now().date())
            # Envia correo de aviso si se realizaron actualizaciones 
            if filas_afectadas > 0:
                cuotas.enviarCorreoAvisoPago(request, cuotasSeleccionadas)
            else:
                raise ValueError("No se realizaron actualizaciones, compruebe los datos datos del formulario.")
            return True
        # Mantener las cuotas como Pendientes si la transacción falló
        elif respuestaTransaccion['status'] == 'FAILED':
            return False

    def get_context_data(self, **kwargs):
        # Obtener los datos del token y la respuesta de la transacción de la sesión
        token = self.request.session.pop('token', None)
        respuestaTransaccion = self.request.session.pop('respuestaTransaccion', None)
        resultadoTransaccion = self.request.session.pop('resultadoTransaccion', None)

        # Crea el contexto de la vista con los datos a renderizar
        contexto = {
            'nameWeb': nameWeb,
            'title': "cuotas",
            # 'front': list(self.front.values('titulo', 'img', 'order')),
            'value': self.front,
            'rol': self.request.user.perfil,
            'create_request': self.request.session.get('create_request'),
            'response': self.request.session.get('response'),
            'token': token,
            'respuestaTransaccion': respuestaTransaccion,
            'resultado_transaccion': 'TRANSACCION TERMINADA EXITOSAMENTE!' if resultadoTransaccion == True else 'OCURRIO UN PROBLEMA EN LE PAGO DE LA(S) CUOTAS, INTENTELO NUEVAMENTE',
        }

        # Obtener cuotas y promoción de descuento anual
        mostrar_promocion, duracion_descuento, cuotas = self.obtenerCuotasSocios(self.request)
        contexto['cuotas'] = cuotas
        contexto['mostrar_promocion'] = mostrar_promocion
        contexto['descuento_anual'] = duracion_descuento.descuento

        # Se eliminan las variables de sesión relacionadas con la transacción para evitar que persistan
        for key in ['create_request', 'response', 'total_pagar', 'descuento']:
            if key in self.request.session:
                del self.request.session[key]

        return contexto


    def get(self, request, *args, **kwargs):
        # Comprobamos si hay un token presente producto de una transaccion
        token = request.GET.get("token_ws")

        if token: 
        # Si hubo una transaccion, procesa su respuesta y actualiza la DB.
            respuestaTransaccion = (Transaction()).commit(token=token)
            resultadoTransaccion = cuotas.actualizaEstadoCuotas(request, respuestaTransaccion)
            # Almacena los datos del token y la respuesta de la transacción en la sesión
            request.session['token'] = token
            request.session['respuestaTransaccion'] = respuestaTransaccion
            request.session['resultadoTransaccion'] = resultadoTransaccion
            
            # Redirigir al usuario a la misma vista usando PRG
            return HttpResponseRedirect(request.path)  # Redirigir a la misma URL sin agregar nada a la URL
        else:
        # Si no hay token presente, renderiza la página usando GET con los parámetros del contexto
            return self.render_to_response(self.get_context_data())
        

    def post(self, request, *args, **kwargs):
        descuento = None  # Inicializamos descuento como None
        # Establecer las variables necesarias que vienen del formulario
        data_str = request.POST.get('data', '[]')
        cuotasSeleccionadas = json.loads(data_str)
        # Almacenar los datos en la sesión del usuario
        request.session['cuotas_seleccionadas'] = cuotasSeleccionadas

        # Resto del código para procesar los datos y obtener el descuento, si está presente
        if 'descuento' in cuotasSeleccionadas[0]:
            descuento_str = cuotasSeleccionadas[0]['descuento']
            if descuento_str is not None:
                try:
                    descuento = int(descuento_str)
                except ValueError as e:
                    print(f'Error: el descuento no es un valor numérico o válido. Detalles: {e}')
                    descuento = 0

        # Sumamos el monto total de las cuotas a pagar y enviamos el correo.
        total_pagar = sum(int(cuota.get('monto_cuota')) for cuota in cuotasSeleccionadas)

        if descuento:
            total_pagar = total_pagar - descuento

        print("Webpay Plus Transaction.create")
        buy_order = str(random.randrange(1000000, 99999999))
        session_id = str(random.randrange(1000000, 99999999))
        amount = str(total_pagar)
        return_url = request.build_absolute_uri(reverse('cuotas'))
        create_request, response = crearTransaccion(buy_order, session_id, amount, return_url)

        # Almacenar los datos en la sesion
        request.session['create_request'] = create_request
        request.session['response'] = response
        request.session['total_pagar'] = total_pagar
        request.session['descuento'] = 0 if descuento == None else descuento
        contexto = {}
        contexto['request'] = create_request
        contexto['response'] = response

        # Redirigir al usuario a una vista intermedia que procesará los datos y realizará la redirección
        return redirect('procesar_transaccion')