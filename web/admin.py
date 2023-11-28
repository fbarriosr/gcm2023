# from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import *


class CuotaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "año", "nombre_mes_display", "mes")

    def nombre_mes_display(self, obj):
        return obj.nombre_mes()

    nombre_mes_display.short_description = "Mes"


# Register your models here.
admin.site.register(Galeria, GaleriaAdmin)
admin.site.register(Links, LinksAdmin)
admin.site.register(Front, FrontAdmin)
admin.site.register(Listado, ListadosAdmin)
admin.site.register(Tipo, TiposAdmin)
admin.site.register(Torneo, TorneoAdmin)
admin.site.register(Club, ClubesAdmin)
admin.site.register(Campeonato, CampeonatosAdmin)
admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(NormaRegla, NormasReglasAdmin)
admin.site.register(CuotaAnual, CuotasAnualesAdmin)
admin.site.register(Cuota, CuotasAdmin)

