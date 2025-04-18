from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, UserLoginForm
from django.contrib import messages


# Vista para el registro
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created successfully!')
            return redirect('home')  # Redirigir a la página principal o cualquier otra página
    else:
        form = UserRegisterForm()

    return render(request, 'auth/register.html', {'form': form})


# Vista para el login
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have logged in successfully!')
                return redirect('home')  # Redirigir a la página principal
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = UserLoginForm()

    return render(request, 'auth/login.html', {'form': form})


def home(request):
    return render(request, 'main_pages/index.html')
