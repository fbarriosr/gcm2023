from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('' , home.as_view(), name = 'home'),
    path('historia' , historia.as_view(), name = 'historia'),
    path('directorio', directorio.as_view(), name='directorio'),
    path('comite', comite.as_view(), name="comite"),
    path('estatutos', estatutos.as_view(), name='estatutos'),
    path('404', NotFound404.as_view(), name='error_404'),
    path('site.webmanifest', manifest, name= 'manifest'),


]
