from django.contrib import admin
from .models import *

admin.site.register(Torneo, TorneoAdmin)
admin.site.register(CardsInicio, CardsInicioAdmin)
admin.site.register(MultimediaImg)
admin.site.register(Multimedia, MultimediaAdmin)
admin.site.register(NoticiaImg)
admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(CuotaAnual, CuotasAnualesAdmin)
admin.site.register(Cuota, CuotasAdmin)
admin.site.register(ElClub, ElClubAdmin)
admin.site.register(Paginas_Socio, Paginas_SocioAdmin)
admin.site.register(Parametro, ParametroAdmin)



