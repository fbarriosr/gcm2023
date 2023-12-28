from django.urls import path
from django.contrib.auth.decorators import login_required
from capitan.views import *

urlpatterns = [   
    path('admin_torneos', torneos.as_view(), name= 'listaTorneosCapitan'),
   
]