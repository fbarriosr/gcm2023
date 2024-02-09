from django.urls import path
from django.contrib.auth.decorators import login_required
from capitan.views import *

urlpatterns = [   
    path('export_csv_cumpleanos',export_csv_cumpleanos, name= 'export_csv_cumpleanos'),
    path('export_csv_cumpleanos_mes',export_csv_cumpleanos_mes, name= 'export_csv_cumpleanos_mes'),
    path('cumpleanos', cumpleanos.as_view(), name= 'cumpleanos'),
    path('export_csv_listado',export_csv_listado, name= 'export_csv_listado'),
    path('salida', salida.as_view(), name= 'salida'),
   
]