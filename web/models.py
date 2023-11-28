# from django.db import models

# Create your models here.

from django.db import models
from django.contrib import admin
from search_admin_autocomplete.admin import SearchAutoCompleteAdmin
from admin_auto_filters.filters import AutocompleteFilter
from autoslug import AutoSlugField
from django.utils import timezone
import uuid
from usuarios.models import Usuario
from .choices import *


# Create your models here.
class UsuarioFilter(AutocompleteFilter):
    title = 'Usuario' # display title
    field_name = 'usuario' # name of the foreign key field

# PLANTILLA PARA A GALERIA EN HOME
class Galeria(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=200, blank=False, null=False)
    img = models.ImageField(upload_to="galeria/")
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Galeria"
        verbose_name_plural = "Galerias"
        ordering = ["order"]

    def __str__(self):
        return self.titulo


class GaleriaAdmin(SearchAutoCompleteAdmin, admin.ModelAdmin):
    search_fields = ["titulo"]
    list_display = ("titulo", "order")
    list_per_page = 10  # No of records per page


# PLANTILLA PARA LOS LINKS EN HOME
class Links(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=200, blank=False, null=False)
    parrafo = models.TextField()
    img = models.ImageField(upload_to="links/")
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"
        ordering = ["order"]

    def __str__(self):
        return self.titulo


class LinksAdmin(SearchAutoCompleteAdmin, admin.ModelAdmin):
    search_fields = ["titulo"]
    list_display = ("titulo", "order")
    list_per_page = 10  # No of records per page


# CONTENIDO PRINCIPAL DE HISTORIA, ETC
class Front(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    img = models.ImageField(upload_to="front/")
    titulo = models.CharField(max_length=200, blank=True, null=True)
    contenido = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)
    file = models.FileField(upload_to="front/files/", max_length=254, blank=True)

    class Meta:
        verbose_name = "Front"
        verbose_name_plural = "Fronts"
        ordering = ["order"]

    def __str__(self):
        return self.titulo


class FrontAdmin(SearchAutoCompleteAdmin, admin.ModelAdmin):
    search_fields = ["titulo"]
    list_display = ("titulo", "order")
    list_per_page = 10


# NOTICIAS DEL SITIO

class Noticia (models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo          = models.CharField(max_length = 200, blank = False, null = False)
    img             = models.ImageField(upload_to='noticias/')
    fecha           = models.DateField()
    resumen         = models.CharField(max_length = 200, blank = False, null = False)
    info            = models.TextField()
    slug            = AutoSlugField(populate_from='titulo')
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


# CLASIFICA A QUE PERTENECEN LAS LISTAS DE IMAGENES DEL MODELO 'LISTA'
class Tipo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo = models.CharField(
        max_length=200, blank=False, null=False, verbose_name="Tipo"
    )
    descripcion = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Tipo"
        verbose_name_plural = "Tipos"
        ordering = ["order"]

    def __str__(self):
        return str(self.tipo)


class TiposAdmin(SearchAutoCompleteAdmin, admin.ModelAdmin):
    search_fields = ["tipo"]
    list_display = ("tipo", "order")
    list_per_page = 10


# ADMINISTRA EL LISTADO DE IMAGENES DE PRESIDENTES, COMITE, ETC...
class Listado (models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo            = models.ForeignKey(Tipo, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Tipo')
    titulo          = models.CharField(max_length=200, blank= False, null = False)
    img             = models.ImageField(upload_to='listado/')
    order           = models.IntegerField(default=0)
    actual          = models.BooleanField(default= False)


    class Meta:
        verbose_name = "Listado"
        verbose_name_plural = "Listados"
        ordering = ["tipo", "order"]

    def __str__(self):
        return self.titulo


class ListadosAdmin(SearchAutoCompleteAdmin, admin.ModelAdmin):

    search_fields   = ['titulo']
    list_display    =('titulo', 'order', 'tipo', 'actual')
    list_per_page   = 10 # No of records per page


# ADMINISTRA LOS CARDS DE TORNEO
class Torneo (models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo          = models.CharField(max_length=200, blank=False, null= False, verbose_name="Titulo")
    direccion       = models.CharField(max_length=200, blank=False, null= False, verbose_name="Direccion")
    region          = models.CharField(max_length=50,choices= regiones, default= 'XIII', verbose_name="Region")
    descripcion     = models.TextField(blank=True)
    img             = models.ImageField(upload_to='torneo/')
    fecha           = models.DateField()
    cupos           = models.IntegerField()
    inscritos       = models.IntegerField(default=0)
    activo          = models.BooleanField(default=True)
    proximo         = models.BooleanField(default=False)
    order           = models.IntegerField(default=0)

    class Meta:
        verbose_name    = 'Torneo'
        verbose_name_plural = 'Torneos'
        ordering    = ['-proximo','activo','fecha']

class TorneoAdmin (SearchAutoCompleteAdmin, admin.ModelAdmin):
    search_fields   = ['titulo']
    list_display    = ('titulo','fecha','region','activo','proximo')
    list_per_page   = 10 # No of records per page


# ADMINISTRA LOS CARDS DE TORNEO
class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(
        max_length=200, blank=False, null=False, verbose_name="Titulo"
    )
    direccion = models.CharField(
        max_length=200, blank=False, null=False, verbose_name="Direccion"
    )
    comuna = models.CharField(
        max_length=200, blank=False, null=False, verbose_name="Comuna"
    )
    region = models.CharField(
        max_length=50, blank=False, null=False, verbose_name="Region"
    )
    descripcion = models.TextField()
    img = models.ImageField(upload_to="cards/")
    fecha = models.DateField()
    cupos = models.IntegerField()
    inscritos = models.IntegerField(default=0)
    activo = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"
        ordering = ["order"]

    def __str__(self):
        return self.titulo

class CardsAdmin(SearchAutoCompleteAdmin, admin.ModelAdmin):
    search_fields = ["titulo"]
    list_display = ("titulo", "order")
    list_per_page = 10  # No of records per page


# LISTADO DE CLUBES DONDE SE REALIZAN LOS TORNEOS, TAL VEZ SE CELEBREN MÁS DE 1 TORNEO POR CLUB
class Club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(
        max_length=50, blank=False, null=False, verbose_name="Nombre del club"
    )
    abreviado = models.CharField(
        max_length=10, blank=False, null=False, verbose_name="Nombre abreviado"
    )
    direccion = models.CharField(
        max_length=200, blank=False, null=False, verbose_name="Direccion"
    )
    comuna = models.CharField(
        max_length=50, blank=False, null=False, verbose_name="Comuna"
    )
    ciudad = models.CharField(
        max_length=50, blank=False, null=False, verbose_name="Ciudad"
    )
    correo = models.EmailField(
        max_length=200, blank=True, null=True, verbose_name="Correo electronico"
    )
    telefono = models.IntegerField(blank=True, null=True, verbose_name="Telefono")
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Club"
        verbose_name_plural = "Clubes"
        ordering = ["order"]

    def __str__(self):
        return self.nombre


class ClubesAdmin(SearchAutoCompleteAdmin, admin.ModelAdmin):
    search_fields = ["nombre"]
    list_display = ("nombre", "order")
    list_per_page = 10


class Campeonato(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(
        max_length=50, blank=False, null=False, verbose_name="Nombre del campeonato"
    )
    fecha = models.DateField(verbose_name="Fecha de torneo")
    club = models.ForeignKey(
        Club, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Club"
    )  # listado de clubes, deberia coincidir con el torneo
    bases = models.FileField(upload_to="bases/")  # bases del toreno, pdf
    #    inscritos       = models.ForeignKey() # listado de inscritos actuales del torneo
    #    salidas         = models.ForeignKey() # esquema de salida de los jugadores en el torneo
    #    resultados      = models.ForeignKey() # listado posiciones del torneo segun distintos parametros
    #    premiacion      = models.ForeignKey() # resumen de los primeros lugares por categoria
    #    galeria         = models.ForeignKey() # galeria de fotos relacionados al torneo
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Campeonato"
        verbose_name_plural = "Campeonatos"
        ordering = ["order"]

    def __str__(self):
        return self.nombre


class CampeonatosAdmin(SearchAutoCompleteAdmin, admin.ModelAdmin):
    search_fields = ["nombre"]
    list_display = ("nombre", "order")
    list_per_page = 10


# ADMINISTRA EL LISTADO DE IMAGENES DE PRESIDENTES, COMITE, ETC...
class NormaRegla(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=200, blank=False, null=False)
    descripcion = models.TextField(
        blank=True, null=True, verbose_name="Descripcion del perfil"
    )
    archivo = models.FileField(upload_to="normas_reglas/")  # normas y reglamentos, pdf
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Norma_Regla"
        verbose_name_plural = "Normas_Reglas"
        ordering = ["titulo", "order"]

    def __str__(self):
        return self.titulo


class NormasReglasAdmin(SearchAutoCompleteAdmin, admin.ModelAdmin):
    search_fields = ["titulo"]
    list_display = ("titulo", "order")
    list_per_page = 10  # No of records per page


# LA ESTRUCTURA DE LAS CUOTAS ANUALES DE LOS SOCIOS DEL CLUB CGM
class CuotaAnual(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    año = models.PositiveIntegerField(verbose_name="Año cuotas")
    monto_cuota = (
        models.IntegerField()
    )  # monto fijo anual aplicable a cada cuota del mes de dicho año.
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "CuotaAnual"
        verbose_name_plural = "CuotasAnuales"
        ordering = ["order"]

    def __str__(self):
        return str(self.año)


class CuotasAnualesAdmin(SearchAutoCompleteAdmin, admin.ModelAdmin):
    search_fields = ["año"]
    list_display = ("año", "order")
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
    list_display = ("año", "mes", "order",'usuario')
    autocomplete_fields = ['usuario']
    list_filter = ('año','usuario')
    list_per_page = 10
