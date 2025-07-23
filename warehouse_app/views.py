from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm


def index(request):
    form = RegisterForm()
    return render(request, 'index.html', {'form': form})


def faq(request):
    return render(request, 'faq.html')


def boxes(request):
    return render(request, 'boxes.html')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'index.html', {'form': form, 'show_modal': True})
    else:
        form = RegisterForm()
    return render(request, 'index.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    return redirect('index')


def logout_view(request):
    logout(request)
    return redirect('index')
