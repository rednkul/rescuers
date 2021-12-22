from django.contrib.auth.forms import AuthenticationForm

from django import forms


class LoginForm(AuthenticationForm):
    class Meta:
        widget = {
            'username': forms.TextInput(attrs={'class': 'form-control border'},),
            'password': forms.TextInput(attrs={'class': 'form-control border'}),

        }