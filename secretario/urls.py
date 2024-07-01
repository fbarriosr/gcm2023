from django.urls import path
from django.contrib.auth.decorators import login_required
from secretario.views import *

urlpatterns = [   
    path('bus', bus.as_view(), name= 'bus'),
    path('auto', auto.as_view(), name= 'auto'),
    path('carro', carro.as_view(), name= 'carro'),
    path('torneo/export_csv_bus',export_csv_bus, name= 'export_csv_bus'),
    path('torneo/export_csv_auto',export_csv_auto, name= 'export_csv_auto'),
    path('torneo/export_csv_carro',export_csv_carro, name= 'export_csv_carro'),
    path('torneo/export_csv_inscritos',export_csv_inscritos, name= 'export_csv_inscritos'),
    path('rankingUpdate', rankingUpdate.as_view(), name= 'rankingUpdate'),
    path('noticiaUpdate', noticiaUpdate.as_view(), name= 'noticiaUpdate'),
    path('noticiaCreate', noticiaCreate.as_view(), name= 'noticiaCreate'),
    path('noticiaDelete', noticiaDelete.as_view(), name= 'noticiaDelete'),
    path('multimediaUpdate', multimediaUpdate.as_view(), name= 'multimediaUpdate'),
    path('multimediaCreate', multimediaCreate.as_view(), name= 'multimediaCreate'),
    path('multimediaDelete', multimediaDelete.as_view(), name= 'multimediaDelete'),
    path('torneoCreate',  torneoCreate.as_view(),  name= 'torneoCreate'),
    path('torneoUpdate',  torneoUpdate.as_view(),  name= 'torneoUpdate'),
    path('torneoDelete',  torneoDelete.as_view(),  name= 'torneoDelete'),  
    path('listarUsuarios', listarUsuarios.as_view(), name= 'listarUsuarios'),
    path('usuarioUpdate', usuarioUpdate.as_view(), name= 'usuarioUpdate'),
    path('usuarioCreate', usuarioCreate.as_view(), name= 'usuarioCreate'),
]