from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('' , home.as_view(), name = 'home'),
    path('historia' , historia.as_view(), name = 'historia'),
    path('noticia/<slug:slug>/' , noticia.as_view(), name = 'noticia'),

    path('noticias', principal_noticias.as_view(), name = 'noticias'),
    path('torneos', torneos.as_view(), name= 'torneos'),

    path('ranking', ranking.as_view(), name= 'ranking'),
    path('404', notFound404.as_view(), name= '404'),

    path('comite', comite.as_view(), name="comite"),
    path('directorio', directorio.as_view(), name='directorio'),
    path('normas_reglas', normas_reglas.as_view(), name='normas_reglas'),
    path('cuotas', cuotas.as_view(), name='cuotas'),
    path('resumen_torneo', torneo_resumen.as_view(), name='torneo_resumen'),

    #path('generar_cuotas/<int:año>/<int:valor>', generar_cuotas, name='generar_cuotas'),
    path('generar_cuotas/', generar_cuotas, name='generar_cuotas'),
    path('generar_cuotas_form/', generar_cuotas_form, name='generar_cuotas_socio'),
    path('generar_cuotas_socio/', generar_cuotas_socio, name='generar_cuotas_socio'),
    path('borrar_cuotas/', borrar_cuotas, name='borrar_cuotas'),
    path('borrar_cuotas_socio/', borrar_cuotas_socio, name='borrar_cuotas_socio'),
]