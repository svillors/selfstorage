from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.validators import RegexValidator


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control border-8 py-3 px-5 fs_24 SelfStorage__bg_lightgrey',
        'placeholder': 'E-mail'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control border-8 py-3 px-5 fs_24 SelfStorage__bg_lightgrey',
        'placeholder': 'Имя пользователя'
    }))

    phone = forms.CharField(
        max_length=20,
        required=True,
        label='Телефон',
        validators=[RegexValidator(r'^(\+?7|8)\d{10}$', message='Введите номер в формате +7XXXXXXXXXX, 7XXXXXXXXXX или 8XXXXXXXXXX')],
        widget=forms.TextInput(attrs={
            'class': 'form-control border-8 py-3 px-5 fs_24 SelfStorage__bg_lightgrey',
            'placeholder': 'Телефон'
        })
    )

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
        fields = ['email', 'username', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit)
        phone = self.cleaned_data.get('phone')
        if commit:
            user.profile.phone = phone
            user.profile.save()
        return user


class LoginForm(forms.Form):
    identifier = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control border-8 mb-4 py-3 px-5 fs_24 SelfStorage__bg_lightgrey",
        'placeholder': 'E-mail / Имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control border-8 mb-4 py-3 px-5 fs_24 SelfStorage__bg_lightgrey',
        'placeholder': 'Пароль'
    }))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control fs_24 ps-2 SelfStorage__input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control fs_24 ps-2 SelfStorage__input'}),
            'phone': forms.TextInput(attrs={'class': 'form-control fs_24 ps-2 SelfStorage__input'}),
        }
