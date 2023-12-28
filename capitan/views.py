from typing import Any
from django.shortcuts import render
from django.views.generic import (
    View,
    TemplateView,
    ListView,
    UpdateView,
    CreateView,
    DeleteView,
    DetailView,
)
from .models import *
from web.models import *
from socios.models import *
from django.core.paginator import Paginator

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy

from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse


from django.shortcuts import HttpResponse
from datetime import datetime
#from .forms import *

from datetime import datetime


nameWeb = "CGM"

class torneos(TemplateView):
    template_name = "views/torneosCapitan.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["nameWeb"] = nameWeb
        contexto["title"] = "torneo"
        mainCard = Torneo.objects.filter(proximo = True)
        torneoCard = Torneo.objects.filter(proximo= False).order_by('-fecha')
        diccionario_fechas = list(Torneo.objects.filter(proximo= False).values('fecha'))

        # Obtener los años de cada fecha en una lista
        anios = [elemento['fecha'].year for elemento in diccionario_fechas]

        # Encontrar el año mínimo y máximo en la lista de años
        anio_minimo = min(anios)
        anio_maximo = max(anios)

        if anio_maximo != anio_minimo:
            contexto['year'] = str(anio_minimo) +'-'+ str(anio_maximo)
        else:
        	contexto['year'] = str(anio_minimo)
        contexto['mainCard'] = mainCard
        contexto['torneoCard'] = torneoCard
        

        return contexto



