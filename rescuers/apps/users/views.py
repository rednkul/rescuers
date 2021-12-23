from django.shortcuts import render

# Create your views here.
from django.contrib.auth.views import LoginView

from .forms import LoginForm


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

