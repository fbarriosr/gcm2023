from django.urls import path, include
from django.contrib.auth.decorators import login_required
from usuarios.views import *

from django.contrib.auth import views as auth_views

urlpatterns = [   
    path('accounts/login/',Login.as_view(), name= 'login'),
    path('logout/', login_required(logoutUsuario), name= 'logout'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]