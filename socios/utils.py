from usuarios.models import Usuario
from .models import *
from .models import CuotaAnual
from django.utils import timezone
from .choices import estado_cuota
from django.http import HttpResponseRedirect, HttpResponse
from .choices import mes_num_texto

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import redirect


# Genera las cuotas de todos los usuarios para el año requerido
def generar_cuotas_grupal(año, valor):
    # Evitamos duplicar datos comprobando que el nuevo año no exista
    c = CuotaAnual.objects.filter(año = año)
    print('ciitec')
    print('año',año)
    print(c)

    if c:
        return 'El año ingresado ya existe'
    
    usuarios = Usuario.objects.all()
    for usuario in usuarios:
        anual, created = CuotaAnual.objects.get_or_create(año=año, monto_cuota=valor)
        for num_cuota in range(1,13):
            mes_cuota = num_cuota + 2 if num_cuota <= 10 else num_cuota - 10
            cuota, created = Cuota.objects.get_or_create(usuario=usuario, año=anual, numero_cuota=num_cuota, mes=mes_cuota, order=num_cuota)
            cuota.save()
        # for mes in range(1,13):
        #     cuota, created = Cuota.objects.get_or_create(usuario=usuario, año=anual, mes=mes)
        #     cuota.save()
    return 'GenerarCuotasAnual ejecutado con exito'


# Genera las cuotas de un nuevo socio para el año en curso si no se especifica uno
def generar_cuotas_individual(rut, año):
    # Verificamos que el usuario exista
    usuario = Usuario.objects.filter(rut=rut).first()
    if usuario is None:
        return f'Usuario {usuario} no encontrado'
    
    # Si no se ingresó el año, se usa el año en curso
    if not año:
        año = timezone.now().year
    
    # Se verifica que el año sea valido o exista
    año = CuotaAnual.objects.filter(año=año).first()
    if año is None:
        return f'Año invalido o aún no se ha registrado el año actual'
    
    # Generamos las 12 cuotas para el usuario    
    for mes in range(1,13):
        # Verificamos que las cuotas no existan para el usuario
        cuota_existe = Cuota.objects.filter(usuario=usuario, año=año, mes=mes).exists()
        
        if not cuota_existe:
            cuota, created = Cuota.objects.get_or_create(usuario=usuario, año=año, mes=mes)
            cuota.save()
    return f'Usuario encontrado, se generaron las cuotas par el año {año}'
        

def borrar_cuotas_grupal(año):
    if not CuotaAnual.objects.filter(año=año):
        return f'El año {año} no existe'
    
    Cuota.objects.filter(año__año=año).delete()
    CuotaAnual.objects.filter(año=año).delete()
    return f'El año {año} y sus cuotas fueron eliminados con éxito!'


def borrar_cuotas_individual(rut, año):
    # Verificamos que el usuario exista
    usuario = Usuario.objects.filter(rut=rut).first()
    if usuario is None:
        return f'Usuario {usuario} no encontrado'
    
    # Si no se ingresó el año, se usa el año en curso
    if not año:
        año = timezone.now().year
    
    # Se verifica que el año sea valido o exista
    año = CuotaAnual.objects.filter(año=año).first()
    if año is None:
        return f'Año invalido o aún no se ha registrado el año actual'
    
    Cuota.objects.filter(usuario=usuario, año=año).delete()
    return f'Las cuotas de {usuario} del año {año} fueron eliminados con éxito!'


def actualiza_cuota(email, año, mes):
    usuario = Usuario.objects.filter(email=email).first()
    print(f"Actualiza_cuota()=> usuario: {usuario}, año: {año}, mes: {mes}") 

    if usuario is None:
        return f'Usuario no encontrado'

    año = CuotaAnual.objects.filter(año=año).first()
    if año is None:
        return f'Año invalido o aún no se ha registrado el año actual'
    
    # Obtén el código de estado correspondiente al valor 'En Revision'
    estado_revision = next((code for code, value in estado_cuota if value == 'En Revision'), None)
    cuota_actualizada = Cuota.objects.filter(mes=mes, usuario=usuario, año=año).update(estado_pago= estado_revision)
    #return f'Cuota Actualizada'
    
    if cuota_actualizada:
        return f' Se actualizó el estado de la cuota existente para el usuario {email}, año {año}, mes {mes} a "En Revisión"'
    else:
        return f'No se encontró una cuota existente para el usuario {email}, año {año}, mes {mes}'
    

# Función para realizar envios de correo
def contact(tipo, nombre=None, asunto=None, mensaje=None, email=None, año=None, mes=None, total_pagar=None):

    if tipo == 'pago_cuota' or tipo == 'pago_cuotas':
        correo = email
        mes = mes
        año = año 
        mes_txt = mes_num_texto[mes]
        total_pagar = total_pagar

        subject ='Aviso solicitud pago de cuota'
        if tipo == 'pago_cuota':
            message = f'El usuario {correo} ha enviado una solicitud de pago para la cuota del mes de {mes_txt} del {año}'
        else:
            message = f'El usuario {correo} ha enviado una solicitud de pago de cuotas por un monto total de {total_pagar}.\n\n'
            message += 'Para más detalle, diríjase a su menú de cuotas.'
        mensaje_ok = f' Se actualizó el estado de la cuota existente para el usuario {email}, año {año}, mes {mes_txt} a "En Revisión"'
   
        template = render_to_string('views/email_template.html', {
        'email': correo,
        'mes': mes,
        'message': message,   
        })

        email = EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER, # deja como remitente al correo configurado del sistema
            ['nicolas.ep.dev@gmail.com']
        )

    elif tipo == 'formulario_contacto':  
        correo = email
        nombre = nombre
        subject = asunto
        message = mensaje
        mensaje_ok = f'Mensaje enviado con exito'

        template = render_to_string('views/email_template.html', {
        'email': correo,
        'mes': mes,
        'message': message,   
        })

        email = EmailMessage(
            subject,
            template,
            correo, # usar como remitente el correo proporcionado en el formulario
            ['nicolas.ep.dev@gmail.com']
        )
  

    email.fail_silently = False
    email.send()
  
    return mensaje_ok
  