from django.db import models
from django.contrib import admin
from search_admin_autocomplete.admin import SearchAutoCompleteAdmin
from admin_auto_filters.filters import AutocompleteFilter
from autoslug import AutoSlugField
from django.utils import timezone
import uuid
from usuarios.models import Usuario
from .choices import estado, regiones, estado_solicitud, estado_cuota
from import_export.admin import ImportExportModelAdmin

def slugify_two_fields(self):
        return "{}_{}-{}-{}".format(self.titulo, self.fecha.day, self.fecha.month, self.fecha.year)

class Noticia (models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo          = models.CharField(max_length = 200, blank = False, null = False)
    img             = models.ImageField(upload_to='noticias/')
    fecha           = models.DateField()
    resumen         = models.CharField(max_length = 200, blank = False, null = False)
    info            = models.TextField()
    slug            = AutoSlugField(populate_from=slugify_two_fields,  unique_with=['titulo','fecha'])
    is_active       = models.BooleanField('Activo',default = False)
    is_aprobado     = models.BooleanField('Aprobado',default = False)
    is_pendiente    = models.BooleanField('Pendiente',default = True)
    img1            = models.ImageField(upload_to='noticias/',blank = True)
    img2            = models.ImageField(upload_to='noticias/',blank = True)
    img3            = models.ImageField(upload_to='noticias/',blank = True)
    img4            = models.ImageField(upload_to='noticias/',blank = True)
    img5            = models.ImageField(upload_to='noticias/',blank = True)
    direccion       = models.CharField(max_length = 200, blank = True, null = False)
    region          = models.CharField(max_length=50,choices= regiones, default= 'XIII', verbose_name="Region")
 
    comentario      = models.TextField(default='Sin comentario')

    class Meta:
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"
        ordering = ["-fecha"]

    def __str__(self):
        return self.titulo


class NoticiaAdmin(SearchAutoCompleteAdmin, admin.ModelAdmin):
    search_fields = ["titulo"]
    list_display = ("titulo", "fecha", "resumen")
    list_per_page = 10  # No of records per page

# ADMINISTRA LOS CARDS DE TORNEO
class Torneo (models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo          = models.CharField(max_length=200, blank=False, null= False, verbose_name="Titulo")
    direccion       = models.CharField(max_length=200, blank=False, null= False, verbose_name="Direccion")
    region          = models.CharField(max_length=50,choices= regiones, default= 'XIII', verbose_name="Region")
    descripcion     = models.TextField(blank=True)
    img             = models.ImageField(upload_to='torneo/')
    fecha           = models.DateField(null=False)
    cupos           = models.IntegerField(default=100)
    inscritos       = models.IntegerField(default=0)
    activo          = models.BooleanField(default=True)
    proximo         = models.BooleanField(default=False)
    abierto         = models.BooleanField(default=True)
    slug            = AutoSlugField(populate_from=slugify_two_fields,  unique_with=['titulo','fecha'])
    bases           = models.FileField(upload_to="torneos/bases/", max_length=254, blank=True)
    resultados      = models.FileField(upload_to="torneos/resultados/", max_length=254, blank=True)
    premiacion      = models.FileField(upload_to="torneos/premiacion/", max_length=254, blank=True)

    def __str__(self):
        return self.titulo + str(self.fecha)

    class Meta:
        verbose_name    = 'Torneo'
        verbose_name_plural = 'Torneos'
        ordering    = ['-fecha']

class TorneoAdmin (ImportExportModelAdmin,SearchAutoCompleteAdmin, admin.ModelAdmin):
    search_fields   = ['titulo']
    list_display    = ('id','slug','titulo','fecha','region','activo','abierto','proximo','cupos','inscritos' )
    list_per_page   = 10 # No of records per page
    list_filter = ('activo','proximo','abierto')


class Solicitud (models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario         = models.ForeignKey(Usuario,on_delete=models.CASCADE, null=True, verbose_name="Usuario") 
    torneo          = models.ForeignKey(Torneo,on_delete=models.CASCADE, null=True, verbose_name="Torneo")
    fecha           = models.DateTimeField(null=False)
    auto            = models.BooleanField(default=False)
    patente         = models.CharField(max_length=12, blank= True , verbose_name="Patente")
    busCGM          = models.BooleanField(default=False)
    carro           = models.BooleanField(default=False)
    indice          = models.IntegerField(blank=True, null=True, verbose_name="Indice")
    acompanantes    = models.TextField(blank=True, verbose_name='¿Con quién va?')
    descripcion     = models.TextField(blank=True, verbose_name='Solicitud')
    deuda_socio     = models.IntegerField(default=0, null=False, verbose_name="Deuda Socio")
    cancela_deuda_socio  = models.BooleanField(default=False)
    recargo         = models.IntegerField(default=0, null=False, verbose_name="Recargo")
    cuota           = models.IntegerField(default=0, null=False, verbose_name="Cuota de Campeonato")
    monto           = models.IntegerField(default=0, null=False, verbose_name="Monto Pagado")
    estado          = models.CharField(max_length=50,choices= estado_solicitud, default= 'P', verbose_name="Estado")
    motivo          = models.TextField(default='',blank=True, verbose_name='Motivo')
    checkCapitan    = models.BooleanField(default=False)
    indiceTorneo    = models.IntegerField(default=0,blank=True, null=True, verbose_name="Indice Torneo")
    hoyoInicial     = models.IntegerField(default=0,blank=True, null=True, verbose_name="Hoyo Inicial")
    suspende        = models.BooleanField(default=False, verbose_name='Suspende Participación' )
    motivoSuspencion= models.TextField(default='',blank=True, verbose_name='Motivo Suspención')


    class Meta:
        verbose_name    = 'Solicitud'
        verbose_name_plural = 'Solicitudes'
        ordering    = ['-fecha']
class SolicitudAdmin (SearchAutoCompleteAdmin, admin.ModelAdmin):
    search_fields   = ['usuario']
    list_display    = ('usuario','torneo','fecha','busCGM','carro','cancela_deuda_socio' ,'monto' , 'estado')
    list_per_page   = 10 # No of records per page
    list_filter = ('usuario','torneo', 'estado')
    autocomplete_fields = ['usuario','torneo']


# LA ESTRUCTURA DE LAS CUOTAS ANUALES DE LOS SOCIOS DEL CLUB CGM
class CuotaAnual(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    año             = models.PositiveIntegerField(verbose_name="Año cuotas")
    monto_cuota     = (models.IntegerField())  # monto fijo anual aplicable a cada cuota del mes de dicho año.
    order           = models.IntegerField(default=0)

    class Meta:
        verbose_name = "CuotaAnual"
        verbose_name_plural = "CuotasAnuales"
        ordering = ["order"]

    def __str__(self):
        return str(self.año)

class CuotasAnualesAdmin(ImportExportModelAdmin, SearchAutoCompleteAdmin, admin.ModelAdmin):
    search_fields = ["año"]
    list_display = ("año", "monto_cuota", "order")
    list_per_page = 10


# LA ESTRUCTURA DE LAS CUOTAS DE LOS SOCIOS DEL CLUB CGM
class Cuota(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mes                     = models.IntegerField()
    año                     = models.ForeignKey(CuotaAnual, blank=True, null=True, on_delete=models.CASCADE)  # monto fijo anual aplicable a cada cuota del mes de dicho año.
    usuario                 = models.ForeignKey(Usuario, blank=False, null=False, on_delete=models.CASCADE, verbose_name="socio club")
    monto_descuento         = models.PositiveIntegerField(blank=True, null=True)  # descuento que se podria aplicar a la cuota
    monto_cargo             = models.PositiveIntegerField(blank=True, null=True)  # monto extra por atraso, castigo..
    monto_pago              = models.PositiveIntegerField(blank=True, null=True)  # monto_pago = monto_cuota - monto_descuento + monto_cargo
    fecha_pago              = models.DateField(blank=True, null=True, verbose_name="Fecha de pago")
    estado_pago             = models.CharField(max_length=1, choices=estado_cuota, default="P", verbose_name="Estado de la cuota")
    order                   = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Cuota"
        verbose_name_plural = "Cuotas"
        ordering = ["año",'mes']

    def nombre_mes(self):
        return timezone.datetime(self.año.año, self.mes, 1).strftime("%B")

    nombre_mes.short_description = "Mes"

    def valor_cuota_mensual(self):
        return self.año.monto_cuota

    def __str__(self):
        return f"{self.usuario.primer_nombre} - {self.año.año} - Mes {self.mes}"


class CuotasAdmin(SearchAutoCompleteAdmin, admin.ModelAdmin):
    search_fields = ["mes"]
    list_display = ('año', 'mes', 'order','usuario', 'estado_pago')
    autocomplete_fields = ['usuario']
    list_filter = ('año','usuario')
    list_per_page = 10
