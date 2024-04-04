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
    #path('generar_cuotas/<int:año>/<int:valor>', generar_cuotas, name='generar_cuotas'),
    path('generar_cuotas_form/', generar_cuotas, name='generar_cuotas_form'),
    path('generar_cuotas2/', generar_cuotas2, name='generar_cuotas2'),
    path('generar_cuotas_socio/', generar_cuotas_socio, name='generar_cuotas_socio'),
    path('borrar_cuotas/', borrar_cuotas, name='borrar_cuotas'),
    path('borrar_cuotas_socio/', borrar_cuotas_socio, name='borrar_cuotas_socio'),
    path('restablecer_cuotas_socio/', restablecer_cuotas_socio, name='restablecer_cuotas_socio'),

    path('contact/', contact, name='contact'),

    path('perfil/', perfil.as_view(), name='perfil'),
    path('password/'   , PasswordUsuario.as_view(), name='cambiar_password'),
    path('export_csv_solicitudesAprobadas/', export_csv_solicitudesAprobadas, name='export_csv_solicitudesAprobadas'),
    
]

