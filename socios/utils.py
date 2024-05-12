from usuarios.models import Usuario
from .models import *
from .models import CuotaAnual
from django.utils import timezone
from .choices import estado_cuota
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .choices import mes_num_texto

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import redirect



# Genera las cuotas de todos los usuarios para el año requerido
def generar_cuotas_grupal(año, monto_cuota, monto_descuento, monto_cargo):
    
    # Verificamos si ya existe una CuotaAnual para el año especificado
    cuota_anual, created = CuotaAnual.objects.get_or_create(año=año, defaults={'monto_cuota': monto_cuota, 'cargo': monto_cargo, 'descuento': monto_descuento})

    # Evitamos errores comprobando que existan usuarios antes de continuar
    if Usuario.objects.exists():
        usuarios = Usuario.objects.all()
        
        # Evitamos duplicados de DescuentoCuota, CargoCuota y CuotaAnual para el mismo año
        cuota_anual, _  = CuotaAnual.objects.get_or_create(año=año, monto_cuota=monto_cuota, cargo=monto_cargo, descuento=monto_descuento)

        # En vez de ingresar los registros 1 a 1 los guardamos en una lista y luego hacemos un volcado a la bd
        cuotas = []
        for usuario in usuarios:

            # Verificamos si ya existe una CuotaAnual para el usuario y el año especificados
            cuota_existente = Cuota.objects.filter(usuario=usuario, año=cuota_anual).exists()
            
            if not cuota_existente:
                for num_cuota in range(1,13):
                    mes_cuota = num_cuota + 2 if num_cuota <= 10 else num_cuota - 10
                    # Cuota.objects.create(usuario=usuario, año=cuota_anual, numero_cuota=num_cuota, mes=mes_cuota, order=num_cuota)
                    cuotas.append(Cuota(usuario=usuario, año=cuota_anual, numero_cuota=num_cuota, mes=mes_cuota, order=num_cuota))
        
        # Solo creamos las cuotas si no existen para el usuario y el año especificados
        if cuotas:
            Cuota.objects.bulk_create(cuotas)
            return 'Operacion exitosa'
        else:
            return 'Las cuotas para el año y usuario especificados ya existen'
    else:
        return 'Deben existir primero usuarios en la BD.'


# Genera las cuotas de un nuevo socio para el año en curso si no se especifica uno
def generar_cuotas_individual(rut, año):
    # Verificamos que el usuario exista
    usuario = Usuario.objects.filter(rut=rut).first()
    if usuario is None:
        return False, f'Usuario {usuario} no encontrado'
    
    # Si no se ingresó el año, se usa el año en curso
    if not año:
        año = timezone.now().year
    
    # Se verifica que el año sea valido o exista
    año = CuotaAnual.objects.filter(año=año).first()
    if año is None:
        return False, f'Año invalido o aún no se ha registrado el año actual'
    
    cuotas = []
    # Generamos las 12 cuotas para el usuario    
    # Verificamos si ya existe una CuotaAnual para el usuario y el año especificados
    cuota_existente = Cuota.objects.filter(usuario=usuario, año=año).exists()
    
    if not cuota_existente:
        for num_cuota in range(1,13):
            mes_cuota = num_cuota + 2 if num_cuota <= 10 else num_cuota - 10
            # Cuota.objects.create(usuario=usuario, año=cuota_anual, numero_cuota=num_cuota, mes=mes_cuota, order=num_cuota)
            cuotas.append(Cuota(usuario=usuario, año=año, numero_cuota=num_cuota, mes=mes_cuota, order=num_cuota))

    # Solo creamos las cuotas si no existen para el usuario y el año especificados
    if cuotas:
        Cuota.objects.bulk_create(cuotas)
        return True, f'Usuario encontrado, se generaron las cuotas par el año {año}'
        

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
        return False, f'Usuario {usuario} no encontrado'
    
    # Si no se ingresó el año, se usa el año en curso
    if not año:
        año = timezone.now().year
    
    # Se verifica que el año sea valido o exista
    año = CuotaAnual.objects.filter(año=año).first()
    if año is None:
        return False, f'Año invalido o aún no se ha registrado el año actual'
    
    Cuota.objects.filter(usuario=usuario, año=año).delete()
    return True, f'Las cuotas de {usuario} del año {año} fueron eliminados con éxito!'


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
    

def restablecer_cuotas_individual(rut, año):
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
    
    # Obtén el código de estado correspondiente al valor 'En Revision'
    estado_revision = next((code for code, value in estado_cuota if value == 'Pendiente'), None)
    Cuota.objects.filter(usuario=usuario, año=año).update(estado_pago= estado_revision)
    return f'Las cuotas de {usuario} del año {año} fueron restablecidas con éxito!'
    

# Función para realizar envios de correo
def contact(tipo, nombre=None, asunto=None, mensaje=None, email=None, año=None, mes=None, total_pagar=None, descuento=None):
    try:
        if tipo == 'pago_cuota' or tipo == 'pago_cuotas':
            correo = email
            mes = mes
            año = año 
            mes_txt = mes_num_texto[mes]
            total_pagar = total_pagar
            descuento = descuento

            print('funcion contact, descuento de:', descuento) 

            subject ='Aviso solicitud pago de cuota'
            if tipo == 'pago_cuota':    
                message = f'El usuario {correo} ha enviado una solicitud de pago para la cuota del mes de {mes_txt} del {año}\n\n'
                message+= f'el monto de la cuota es de {total_pagar}, para más detalla diríjase a su menú de cuotas.'
            elif tipo == 'pago_cuotas':
                if descuento:
                    message = f'El usuario {correo} ha enviado una solicitud para pagar el año {año}.\n\n'
                    message += f'el monto es de {total_pagar} menos descuento de {descuento}, total a pagar: {total_pagar - descuento}.'
                else:
                    message = f'El usuario {correo} ha enviado una solicitud de pago de cuotas por un monto total de {total_pagar}.\n\n'
                    message += 'Para más detalle, diríjase a su menú de cuotas.'
            mensaje_ok = f' Se actualizó el estado de la cuota existente para el usuario {email}, año {año}, mes {mes_txt} a "En Revisión"'

            template = render_to_string('socio/views/email_template.html', {
            'email': correo,
            'mes': mes,
            'message': message,   
            })

            email = EmailMessage(
                subject,
                template,
                settings.EMAIL_HOST_USER, # deja como remitente al correo configurado del sistema
                ['nicolas.ep.dev@gmail.com', 'cgm.tesorero@gmail.com']
            )

        elif tipo == 'formulario_contacto':  
            correo = email
            nombre = nombre
            subject = asunto
            message = mensaje
            mensaje_ok = f'Mensaje enviado con exito'

            template = render_to_string('socio/views/email_template.html', {
            'email': correo,
            'mes': mes,
            'message': message,   
            })

            email = EmailMessage(
                subject,
                template,
                correo, # usar como remitente el correo proporcionado en el formulario
                ['nicolas.ep.dev@gmail.com', 'cgm.secretario@gmail.com']
            )

        email.fail_silently = False
        email.send()
  
        return mensaje_ok
    except Exception as e:
        error_message = str(e)
        print(f'Error en el envio del correo: {error_message}')

        return f"Error en el envio del correo: {error_message}"
