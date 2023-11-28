from django.urls import path
from django.contrib.auth.decorators import login_required
from usuarios.views import *

urlpatterns = [   
    path('accounts/login/',Login.as_view(), name= 'login'),
    path('logout/', login_required(logoutUsuario), name= 'logout'),
]