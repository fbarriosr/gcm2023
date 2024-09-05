from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy



class AutentificadoMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')

class SociosMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.perfil != 'I':
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')

class SecretarioMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.perfil == "SECR" or request.user.perfil == "SUPER" :
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')

class CapitanMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.perfil == "CAP" or request.user.perfil == "SUPER" :
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')

class TesoreroMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.perfil == "T" or request.user.perfil == "SUPER" :
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')