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

from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required

from django.shortcuts import HttpResponse
from datetime import datetime
from web.mixins import *
from .forms import *
from .utils import *
from .choices import estado_cuota
from datetime import datetime


nameWeb = "CGM"

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
class noticias(TemplateView):
    model = Noticia
    template_name = "views/noticias.html"
    
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
        mainCard = Torneo.objects.filter(activo=True).filter(proximo = True)
        torneoCard = Torneo.objects.filter(activo=True).filter(proximo= False).order_by('-fecha')
        diccionario_fechas = list(Torneo.objects.filter(activo=True).filter(proximo= False).values('fecha'))

        # Obtener los años de cada fecha en una lista
        anios = [elemento['fecha'].year for elemento in diccionario_fechas]

        # Encontrar el año mínimo y máximo en la lista de años
        anio_minimo = min(anios)
        anio_maximo = max(anios)

        if anio_maximo != anio_minimo:
            contexto['year'] = str(anio_minimo) +'-'+ str(anio_maximo)
        else:
        	contexto['year'] = str(anio_minimo)
        contexto['mainCard'] = mainCard
        contexto['torneoCard'] = torneoCard
        

        return contexto

# Create your views here.
class torneo(DetailView):
    model = Torneo
    template_name = "views/torneo.html"
    
    def get(self, *args, **kwargs):
        dato =  self.get_object()
        torneoid = dato[0].id
        torneoEstado = dato[0].abierto
        solicitud = Solicitud.objects.filter(usuario__email=self.request.user.email).filter(torneo__id=torneoid).order_by('-fecha')
        
        if (torneoEstado==True): #torneo abierto

            if (len(solicitud)==0 ): # solicitud
                response = redirect('solicitud') # para inscribir
                response.set_cookie('torneo', torneoid)
                return response
            else:
                if(solicitud[0].estado =='S'): #arrependido
                    response = redirect('solicitud') # para inscribir
                    response.set_cookie('torneo', torneoid)
                    return response 
                else: 
                    response = super().get( *args, **kwargs)
                    response.set_cookie('torneo', torneoid)
                    return response  
        else: 
            response = super().get( *args, **kwargs)
            response.set_cookie('torneo', torneoid)
            return response
        
       
    def get_context_data(self, **kwargs):

        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        dato =  self.get_object()
        torneoid = dato[0].id
        torneoEstado = dato[0].abierto
        contexto['torneoEstado'] = torneoEstado
        contexto['torneoImg']= dato[0].img
        contexto['torneoFecha']= str(dato[0].fecha)
        contexto['torneoLugar']= dato[0].direccion+'-' + dato[0].region
        contexto['torneoInscritos']= dato[0].inscritos
        contexto['torneoCupos']= dato[0].cupos
        solicitud = Solicitud.objects.filter(usuario__email=self.request.user.email).filter(torneo__id=torneoid).order_by('-fecha') #ultima solicitud
        
        if (len(solicitud)==0 ): # no hay solicitud
            if (torneoEstado==False): #torneo Cerrado
                contexto['solicitudEstado']= 'C'
                contexto['nombreTorneo'] = dato[0].titulo
        else:  # si hay solictud
            contexto['solicitud']= solicitud[0]
            contexto['solicitudEstado']=solicitud[0].estado
            if (solicitud[0].estado == 'A'):
                contexto['bases']= solicitud[0].torneo.bases
                contexto['premiacion']= solicitud[0].torneo.premiacion
                contexto['resultados']= solicitud[0].torneo.resultados
                contexto['listadoAceptados'] = Solicitud.objects.filter(torneo__id=torneoid).filter(estado='A').order_by('usuario__apellido_paterno')
            elif (solicitud[0].estado == 'S'):
                if (torneoEstado==False): #torneo Cerrado
                    contexto['solicitudEstado']= 'C'
                    contexto['nombreTorneo'] = dato[0].titulo

        return contexto

    

    def get_object(self, **kwargs):
        print('slug', self.kwargs.get('slug', None))
        slug =  self.model.objects.filter(slug = self.kwargs.get('slug', None))
        return slug


class crearSolicitud(CreateView):
    model = Solicitud
    form_class = FormularioSolicitudView
    template_name = "views/solicitud.html"

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

     
        return contexto

    def get_object(self, **kwargs):
        torneo= self.request.COOKIES.get('torneo') 
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


class crearSolicitudSuspender(CreateView):
    model = Solicitud
    form_class = FormularioSolicitudSuspenderCreate
    template_name = "views/suspender.html"

    def get_context_data(self,**kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['nameWeb']     =  nameWeb
        
        contexto['btnAction']   = 'Enviar'
        contexto['urlForm']     = self.request.path

        torneo   = self.get_object()
        contexto['torneo'] = torneo
        torneoTitulo = str(torneo.titulo).upper().replace('TORNEO','') 
        contexto['titulo'] = 'SOLICITUD DE SUSPENCION PARTICIPACIÓN '+ torneoTitulo
     
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

class ranking(TemplateView):
    template_name = "views/ranking.html"
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb

        contexto["title"] = "ranking"
        front = Front.objects.filter(titulo="ranking")
        contexto['front']  = list(front.values('titulo','img', 'contenido', 'order','file'))
        
        return contexto

# LA ESTRUCTURA DE LAS CUOTAS DE LOS SOCIOS DEL CLUB CGM

class cuotas_admin(TemplateView, View):
    template_name = "views/cuotas_admin.html"

    def get_context_data(self, **kwargs):
        contexto =  super().get_context_data(**kwargs)
        contexto['nameWeb'] = nameWeb
        contexto['title'] = 'cuotas_admin'
        contexto['mensaje'] = 'holi'

        cuotas = Cuota.objects.all().select_related('usuario', 'año')
        front = Front.objects.filter(titulo="cuotas")
        
        # Obtener los años de las cuotas del socio para el filtro por año en cuotas.html
        años_cuotas_socio = Cuota.objects.values('año__año').distinct().order_by('año__año')
        años_cuotas_socio = sorted([año['año__año'] for año in años_cuotas_socio], reverse=True)

        # Incluir el valor del estado de la cuota, reemplazando la letra por el nombre
        estado_dict = dict(estado)
        for cuota in cuotas:
            if cuota.usuario.estado in estado_dict:
                nuevo_estado = estado_dict[cuota.usuario.estado]
                cuota.usuario.estado_txt= nuevo_estado
                cuota.save()
                #print(f'estado cambiado a: {nuevo_estado}') 

        usuarios_con_cuotas = Usuario.objects.filter(cuota__isnull=False).distinct()
        listado_usuarios = usuarios_con_cuotas.values_list('email', flat=True).order_by('-email')

        print(f'listado usuarios: {listado_usuarios}') 

        contexto['cuotas'] = cuotas
        contexto['front'] = list(front.values('titulo','img', 'contenido', 'order','file'))
        contexto['años_cuotas_socio'] = años_cuotas_socio
        contexto['listado_usuarios'] = listado_usuarios
        return contexto


class cuotas_admin2(TemplateView, View):
    template_name = "views/cuotas_admin2.html"

    def get_context_data(self, **kwargs):
        año_filtro = 2022
        contexto =  super().get_context_data(**kwargs)
        contexto['nameWeb'] = nameWeb
        contexto['title']   = 'cuotas_admin'
        front = Front.objects.filter(titulo="cuotas")

        pendientes  = Cuota.objects.filter(estado_pago='P', año__año=año_filtro).count()
        aprobadas   = Cuota.objects.filter(estado_pago='E', año__año=año_filtro).count()
        rechazadas  = Cuota.objects.filter(estado_pago='R', año__año=año_filtro).count()

        contexto['pendientes']  = pendientes
        contexto['aprobadas']   = aprobadas
        contexto['rechazadas']  = rechazadas
        contexto['front'] = list(front.values('titulo','img', 'contenido', 'order','file'))

        return contexto

class cuotas_admin_mod(TemplateView, View):
    template_name = "views/cuotas_admin_mod.html"

    def post(self, request, *args, **kwargs):
        filtro_cuota    = request.POST.get('filtro', '') # mantiene en la plantilla el filtro del tipo de cuota mostrada
        id_cuota_modificar = request.POST.get('id_cuota_mod', None) 
        valor_cuota_modificar           = request.POST.get('value', None)
        print(f'filtro cuota: {filtro_cuota}') 
        print(f'id cuota a modificar: {id_cuota_modificar}')   
        print(f'valor de la cuota a modificar: {valor_cuota_modificar}')  

        if len(filtro_cuota)> 1:
            filtro_cuota = dict((v, k) for k,v in estado_cuota).get(filtro_cuota, None)  
            print(f'filtro cuota en formato texto, se cambió a: {filtro_cuota}')  
        else:
            print(f'filtro cuota en formato letra, no se hace nada: {filtro_cuota}')

        # Actualizar el estado de la cuota
        if id_cuota_modificar is not None and valor_cuota_modificar is not None:
            # print('se ejecutó la actualizacion de la cuota')
            cuota_seleccionada = Cuota.objects.get(id=id_cuota_modificar)
            cuota_seleccionada.estado_pago = valor_cuota_modificar
            cuota_seleccionada.save()            
            
        contexto = self.get_context_data(filtro_cuota=filtro_cuota)

        return self.render_to_response(contexto)   
        
    def get_context_data(self, **kwargs):
        print('se ejecuto la vista cuotas_admin_mod')
        contexto =  super().get_context_data(**kwargs)
        filtro_cuota = kwargs.get('filtro_cuota','')         
        contexto['nameWeb'] = nameWeb
        contexto['title'] = 'cuotas_admin_mod'
        

        front = Front.objects.filter(titulo="cuotas")
        cuotas = Cuota.objects.filter(estado_pago=filtro_cuota).select_related('usuario', 'año')

        # Obtener los años de las cuotas del socio para el filtro por año en cuotas.html
        años_cuotas_socio = Cuota.objects.values('año__año').distinct().order_by('año__año')
        años_cuotas_socio = sorted([año['año__año'] for año in años_cuotas_socio], reverse=True)

        estado_dict = dict(estado)
        # Incluir el valor del estado del usuario/socio, reemplazando la letra por el nombre
        for cuota in cuotas:
            if cuota.usuario.estado in estado_dict:
                cuota.usuario.estado_txt = estado_dict[cuota.usuario.estado]   

        # Obtener una lista ordenada de los socios con cuotas asignadas
        usuarios_con_cuotas = Usuario.objects.filter(cuota__isnull=False).distinct()
        listado_usuarios = usuarios_con_cuotas.values_list('email', flat=True).order_by('-email')

        contexto['cuotas'] = cuotas
        contexto['front'] = list(front.values('titulo','img', 'contenido', 'order','file'))
        contexto['años_cuotas_socio'] = años_cuotas_socio
        contexto['listado_usuarios'] = listado_usuarios
        # print(f'valor filtro_cuota: {filtro_cuota}') 
        contexto['estado_cuota'] = dict(estado_cuota).get(filtro_cuota, None)
        return contexto

#@login_required Si se usa con request, sin heredar de vistas
@method_decorator(login_required, name='dispatch')
class cuotas(TemplateView, View):
    template_name = "views/cuotas.html"
    rut = None
    año_filtro = 2000
    is_contact = False

    # Para cambiar el estado de variables que se modifican desde otras funciones
    @classmethod
    def set_año_filtro(cls, año):
        cls.año_filtro = año

    @classmethod
    def get_año_filtro(cls):
        return cls.año_filtro
    
    @classmethod
    def set_contact(cls, contact):
        cls.is_contact = contact

    @classmethod 
    def get_contact(cls):
        return cls.is_contact 

    def get(self, request, *args, **kwargs):
        # Obtener los años de las cuotas del socio para el filtro por año en cuotas.html
        años_cuotas_socio = Cuota.objects.values('año__año').distinct().order_by('año__año')
        años_cuotas_socio = sorted([año['año__año'] for año in años_cuotas_socio], reverse=True)

        usuario = self.request.user
        #print(f'usuario: {type(usuario)}')

        for campo in usuario._meta.fields:
            nombre_campo = campo.name
            valor_campo = getattr(usuario, nombre_campo)
            #print(f"{nombre_campo}: {valor_campo}") 

        self.rut = usuario.rut

        # Obtén el año de la clase o usa el valor predeterminado
        self.año_filtro = self.get_año_filtro()
        if self.is_contact == False:
            self.año_filtro = años_cuotas_socio[0] 
            
        # Restablecer is_contact después de su uso
        self.is_contact = False
        self.set_contact(self.is_contact)

        # Establecer los QuerySet de front y Cuotas
        front = Front.objects.filter(titulo="cuotas")
        cuotas = Cuota.objects.filter(usuario__rut=self.rut).select_related('usuario')

        # Crear una lista de objetos datetime para representar los meses del año
        mes_cuota = [datetime(self.año_filtro, mes, 1) for mes in range(1, 13)]

        # Añadir el campo 'mes_datetime' a cada instancia de Cuota
        for cuota in cuotas:
            cuota.mes_cuota = mes_cuota[cuota.mes - 1]   

        # Crear el contexto de la vista con los datos a renderizar
        contexto = {
            "nameWeb": nameWeb,
            "title": "cuotas",
            "front": list(front.values('titulo', 'img', 'contenido', 'order','file')),
            "cuotas": cuotas,
            "años_cuotas_socio": años_cuotas_socio,
            "año_filtro": self.año_filtro,
        }

        # Agregar barra inicial a la ruta de la imagen en el contexto
        for item in contexto["front"]:
            item["img"] = f"{item['img']}"

        return self.render_to_response(contexto)
    
    def post(self, request, *args, **kwargs): 
        # Verificar que se haya ejecutado el metodo POST antes de procesar
        if request.method == 'POST':

            # Establecer las variables necesarias
            email = request.POST.get('email')
            mes = int(request.POST.get('mes'))
            año = int(request.POST.get('año_seleccionado'))
            usuario = Usuario.objects.filter(email=email).first()
            año_contact = CuotaAnual.objects.filter(año=año).first()
            
            # Verificar que coincida el usuario
            if usuario is None:
                return f'Usuario no encontrado'

            # Verificar que exista el año de la cuota
            if año_contact is None:
                return f'Año invalido o aún no se ha registrado el año actual'
            
            # Obtén el código de estado correspondiente al valor 'En Revision'
            estado_revision = next((code for code, value in estado_cuota if value == 'En Revision'), None) 
            filas_afectadas = Cuota.objects.filter(mes=mes, usuario=usuario, año__año=año).update(estado_pago= estado_revision)
            
            # Verificar que se haya actualizado la cuota antes de enviar el correo
            if filas_afectadas > 0: 
                # Invocar a la funcion Contact para que envie el correo de aviso
                resultado = contact(email, año_contact, mes) 
            else:
                resultado = 'No se realizaron actualizaciones. Puede que no haya coincidencia con los criterios de filtro'

            # Establecer un mensaje de aviso al volver a la plantilla html
            messages.success(request, resultado)

            # Configurar el año en la clase Cuotas antes de redirigir
            cuotas.set_año_filtro(año)
            # Avisamos que se ejecutó la función Contact para que no se pierda el año seleccionado al volver a la plantilla
            cuotas.set_contact(True)

            return redirect('cuotas')

        return HttpResponse(f'algo anda mal')