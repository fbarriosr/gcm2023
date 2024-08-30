from django.urls import path
from django.contrib.auth.decorators import login_required
from tesorero.views import *

urlpatterns = [   

    path('resumen_cuotas', resumenCuotas.as_view(), name='resumenCuotas'),
    path('export_csv_solicitudes', export_csv_solicitudes, name='export_csv_solicitudes'),
    path('cuotas_admin/', cuotas_admin.as_view(), name='cuotas_admin'),
    path('resumen_cuotas', resumenCuotas.as_view(), name='resumenCuotas'),
    path('cuotas_admin/', cuotas_admin.as_view(), name='cuotas_admin'),
    path('exportar-resumen-cuotas/', export_csv_resumen_cuotas, name='exportar_resumen_cuotas'),

]