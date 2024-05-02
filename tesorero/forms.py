from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django import forms
from socios.models import *


