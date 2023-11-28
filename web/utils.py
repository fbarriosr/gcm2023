from .models import Usuario, Cuota, CuotaAnual
from django.utils import timezone


# Genera las cuotas de todos los usuarios para el año requerido
def generar_cuotas_grupal(año, valor):
    # Evitamos duplicar datos comprobando que el nuevo año no exista
    if CuotaAnual.objects.filter(año = año):
        return 'El año ingresado ya existe'
    
    usuarios = Usuario.objects.all()
    for usuario in usuarios:
        anual, created = CuotaAnual.objects.get_or_create(año=año, monto_cuota=valor)
        for mes in range(1,13):
            cuota, created = Cuota.objects.get_or_create(usuario=usuario, año=anual, mes=mes)
            cuota.save()
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