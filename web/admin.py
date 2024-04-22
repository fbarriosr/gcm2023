# from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Galeria, GaleriaAdmin)
admin.site.register(Links, LinksAdmin)
admin.site.register(Paginas_Web, Paginas_WebAdmin)
admin.site.register(Listado, ListadosAdmin)
admin.site.register(Tipo, TiposAdmin)
