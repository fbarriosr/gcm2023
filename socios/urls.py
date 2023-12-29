from django.urls import path
from django.contrib.auth.decorators import login_required
from socios.views import *

urlpatterns = [   
    path('torneos', torneos.as_view(), name= 'torneos'),
    path('torneo/<slug:slug>/', torneo.as_view(), name='torneo'),

    path('noticias', noticias.as_view(), name = 'noticias'),
    path('noticia/<slug:slug>/' , noticia.as_view(), name = 'noticia'),
    
    path('ranking', ranking.as_view(), name= 'ranking'),
    path('torneo/solicitud', crearSolicitud.as_view(), name= 'solicitud'),
    path('torneo/suspender', crearSolicitudSuspender.as_view(), name= 'suspender'),


    path('cuotas/', cuotas.as_view(), name='cuotas'),
    #tesorero
    path('cuotas_admin/', cuotas_admin.as_view(), name='cuotas_admin'),
    path('cuotas_admin2/', cuotas_admin2.as_view(), name='cuotas_admin2'),
    path('cuotas_admin_mod/', cuotas_admin_mod.as_view(), name='cuotas_admin_mod'),

    #path('generar_cuotas/<int:año>/<int:valor>', generar_cuotas, name='generar_cuotas'),
    path('generar_cuotas/', generar_cuotas, name='generar_cuotas'),
    path('generar_cuotas_form/', generar_cuotas_form, name='generar_cuotas_socio'),
    path('generar_cuotas_socio/', generar_cuotas_socio, name='generar_cuotas_socio'),
    path('borrar_cuotas/', borrar_cuotas, name='borrar_cuotas'),
    path('borrar_cuotas_socio/', borrar_cuotas_socio, name='borrar_cuotas_socio'),

    path('contact/', contact, name='contact'),
    
]

