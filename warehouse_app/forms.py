from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control border-8 py-3 px-5 fs_24 SelfStorage__bg_lightgrey',
        'placeholder': 'E-mail'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control border-8 py-3 px-5 fs_24 SelfStorage__bg_lightgrey',
        'placeholder': 'Имя пользователя'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control border-8 py-3 px-5 fs_24 SelfStorage__bg_lightgrey',
        'placeholder': 'Пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control border-8 py-3 px-5 fs_24 SelfStorage__bg_lightgrey',
        'placeholder': 'Подтвердите пароль'
    }))

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class LoginForm(forms.Form):
    identifier = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control border-8 mb-4 py-3 px-5 fs_24 SelfStorage__bg_lightgrey",
        'placeholder': 'E-mail / Имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control border-8 mb-4 py-3 px-5 fs_24 SelfStorage__bg_lightgrey',
        'placeholder': 'Пароль'
    }))
