from django import forms
from django_recaptcha.fields import ReCaptchaField

class FormHome(forms.Form):
    nombre = forms.CharField()
    email = forms.CharField()
    asunto = forms.CharField()
    mensaje = forms.CharField(widget=forms.Textarea)
    captcha = ReCaptchaField()