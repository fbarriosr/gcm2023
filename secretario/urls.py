from django.urls import path
from django.contrib.auth.decorators import login_required
from secretario.views import *

urlpatterns = [   
    path('torneo/bus', bus.as_view(), name= 'bus'),
    path('torneo/auto', auto.as_view(), name= 'auto'),
]