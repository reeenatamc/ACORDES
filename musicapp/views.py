# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages


# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from musicapp.forms import UserRegistrationForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu cuenta ha sido creada con éxito. Ahora puedes iniciar sesión.')
            return redirect('login')  # Redirige al login después de registrarse
    else:
        form = UserRegistrationForm()

    return render(request, 'auth/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenido de nuevo, {user.username}!')
            return redirect('home')  # Cambia 'home' por la vista de inicio
        else:
            messages.error(request, 'Error en los datos, por favor verifica.')
    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})

@login_required(login_url='auth/login.html')
def home(request):
    return render(request, 'main_pages/index.html')

# Create your views here.
