from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy



class SocioMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')

class SecretarioMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.perfil.perfil == "Secretario" or request.user.perfil.perfil == "Super Usuario" :
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')

class CapitanMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.perfil.perfil == "Capitan" or request.user.perfil.perfil == "Super Usuario" :
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')

class TesoreroMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.perfil.perfil == "Tesorero" or request.user.perfil.perfil == "Super Usuario" :
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')