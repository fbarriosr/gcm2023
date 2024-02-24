from django.contrib import admin
from .models import *


admin.site.register(Torneo, TorneoAdmin)
admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(CuotaAnual, CuotasAnualesAdmin)
admin.site.register(Cuota, CuotasAdmin)



