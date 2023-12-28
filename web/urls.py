from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('' , home.as_view(), name = 'home'),
    path('historia' , historia.as_view(), name = 'historia'),
    path('directorio', directorio.as_view(), name='directorio'),
    path('comite', comite.as_view(), name="comite"),
    path('404', notFound404.as_view(), name= '404'),
    path('normas_reglas', normas_reglas.as_view(), name='normas_reglas'),
    

    
]