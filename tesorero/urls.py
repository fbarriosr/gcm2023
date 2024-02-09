from django.urls import path
from django.contrib.auth.decorators import login_required
from tesorero.views import *

urlpatterns = [   
    #path('solicitudUpdate', solicitudUpdate.as_view(), name= 'solicitudUpdate'),
    path('solicitudes', solicitudHome.as_view(), name= 'solicitudes'),
    path('listarSolicitudes', listarSolicitudes.as_view(), name= 'listarSolicitudes'),
    path('solicitudUpdate', solicitudUpdate.as_view(), name= 'solicitudUpdate'),


]