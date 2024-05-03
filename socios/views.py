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

from itertools import chain
from transbank.webpay.webpay_plus.transaction import Transaction
import logging, random, json, requests , csv

logger = logging.getLogger(__name__)

nameWeb = "CGM"

def crearTransaccion(buy_order, session_id, amount, return_url):
    create_request = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url
    }

    response = (Transaction()).create(buy_order, session_id, amount, return_url)
    print(f'response tipo {type(response)}')
    print(f'response {response}')
    print(f'url: {response["url"]}')
    print(f'token: {response["token"]}')

    token_ws=response["token"]
    url = response["url"]
    redirect_url = f'{url}?token_ws={token_ws}'
    # response = requests.post(url, data={'token_ws': token_ws})
    print(f'redirect url: {redirect_url}')

    return create_request, response

def procesar_transaccion(request):
    # Obtener los datos de la sesión
    create_request = request.session.get('create_request')
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
 
class perfil(SocioMixin,UpdateView):

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
class multimedia(SocioMixin,DetailView):
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
class multimedias(SocioMixin,TemplateView):
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



class inicio(SocioMixin,TemplateView):
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


class torneos(SocioMixin,TemplateView):
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


class crearSolicitud(SocioMixin,CreateView):
    model = Solicitud
    form_class = FormularioSolicitudView
    template_name = "socio/views/solicitud.html"

    def get_form(self, form_class=None):

        deuda_socio = 3
        recargo = 5000
        cuota = 250000000

        form = super().get_form(form_class)

        form.fields['deuda_socio'].initial = deuda_socio
        form.fields['recargo'].initial = recargo
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
                <strong>El Capitan</strong>"""

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
            cuota        = form.cleaned_data.get('cuota'),
            monto        = form.cleaned_data.get('monto'),


            busCGM       = busCGM[0]
            auto         = auto[0]
            patente      = patente[0]
            carro        = carro[0]
            acompanantes = acompanantes[0]
            indice       = indice[0]
            
            deuda_socio  = deuda_socio[0]
            cancela_deuda_socio = cancela_deuda_socio[0]
            recargo      = recargo[0]
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
            request.session['cuota'] = cuota 
            request.session['monto'] = monto 

            

            # Redirigir a la vista de procesamiento de transacción
            return redirect('procesar_transaccion')
            
            
        else:
            print('errorAqui')
            mensaje = 'Error:'
            error = form.errors
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 400
            return response
      

class inscritos(SocioMixin, TemplateView):
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


class ranking(SocioMixin,TemplateView):
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
    
        años_cuotas_socio = datos['años_cuotas_socio']
        listado_usuarios = datos['listado_usuarios']


        contexto = {
            'nameWeb': nameWeb,
            'title': 'cuotas_admin_mod',
            'rol': self.request.user.perfil,
            'datos': cuotas,
            'cuotas': cuotas,
            'años_cuotas_socio': años_cuotas_socio,
            'listado_usuarios': listado_usuarios,
        }
        
        dato = Paginas_Socio.objects.get(tipo ="C")
        contexto['value']  = dato
        contexto["title"] = dato.tituloPestana

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
        front = Paginas_Socio.objects.filter(titulo="cuotas")
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
            "front": list(front.values('titulo', 'img', 'contenido','file')),
            "cuotas": cuotas,
            "mostrar_promocion": mostrar_promocion,
            "descuento_anual": duracion_descuento.descuento,
            "rol": self.request.user.perfil
        }
        dato = Paginas_Socio.objects.get(tipo ="C")
        contexto['value']  = dato
        contexto["title"] = dato.tituloPestana
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