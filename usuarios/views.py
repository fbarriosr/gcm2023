from django.shortcuts import render
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

from .forms import *


nameWeb = "CGM"

# Create your views here.
class Login(FormView):
    
    template_name = 'views/login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('home')
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    def dispatch(self,request,*args,**kwargs):

        return super(Login,self).dispatch(request,*args,**kwargs)
    
    def form_valid(self,form):
   
        login(self.request,form.get_user())
        
        return super(Login,self).form_valid(form)

    def get(self, request, *args, **kwargs):
        #form_class = self.get_form_class()
        #form = self.get_form(form_class)
        form = self.form_class(initial=self.initial)
        contexto = super(Login, self).get_context_data(**kwargs)

        contexto['nameWeb'] = nameWeb
        contexto['title'] = 'ACCESO AL CLUB' 
        contexto['loginClass'] = 'loginClass'

        contexto['error'] = False

        return self.render_to_response(contexto)

    def form_invalid(self, form, **kwargs):
   
        contexto =  super(Login, self).get_context_data(**kwargs)
        contexto['nameWeb'] = nameWeb
        contexto['title'] = 'Error'
        contexto['loginClass'] = 'loginClass'
        contexto['error'] = True
        return self.render_to_response(contexto)

def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login')