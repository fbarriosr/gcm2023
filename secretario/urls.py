from django.urls import path
from django.contrib.auth.decorators import login_required
from secretario.views import *

urlpatterns = [   
    path('torneo/bus', bus.as_view(), name= 'bus'),
    path('torneo/auto', auto.as_view(), name= 'auto'),
    path('torneo/export_csv_bus',export_csv_bus, name= 'export_csv_bus'),
    path('torneo/export_csv_auto',export_csv_auto, name= 'export_csv_auto'),

    
]