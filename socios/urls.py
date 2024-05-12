from django.urls import path
from django.contrib.auth.decorators import login_required
from socios.views import *

urlpatterns = [  
    path('inicio', inicio.as_view(), name= 'inicio'), 
    path('calendario', torneos.as_view(), name= 'torneos'),
    path('multimedias', multimedias.as_view(), name = 'multimedias'),
    path('multimedia/<slug:slug>/' , multimedia.as_view(), name = 'multimedia'),
    path('noticias', noticias.as_view(), name = 'noticias'),
    path('noticia/<slug:slug>/' , noticia.as_view(), name = 'noticia'),
    path('ranking', ranking.as_view(), name= 'ranking'),
    
    path('solicitud', crearSolicitud.as_view(), name= 'solicitud'),
    path('inscritos', inscritos.as_view(), name= 'inscritos'),
    path('procesar-transaccion/', procesar_transaccion, name='procesar_transaccion'),
    path('cuotas/', cuotas.as_view(), name='cuotas'),
     # tesorero
    path('operaciones_cuotas/', OperacionesCuotasView.as_view(), name='operaciones_cuotas'),
    path('contact/', contact, name='contact'),

    path('perfil/', perfil.as_view(), name='perfil'),
    path('password/'   , PasswordUsuario.as_view(), name='cambiar_password'),
    path('export_csv_solicitudesAprobadas/', export_csv_solicitudesAprobadas, name='export_csv_solicitudesAprobadas'),
    
]

