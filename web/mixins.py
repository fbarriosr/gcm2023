from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy



class SocioMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')