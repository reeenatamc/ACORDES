from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from musicapp.forms import PromptForm
from musicapp.models import UserPrompt


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Esto inicia sesión al usuario después de registrarse
            return redirect('home')  # Redirige al usuario a la página principal o donde desees
    else:
        form = UserCreationForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirige al home o donde quieras
    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})


class PromptFormView(FormView):
    template_name = 'main_pages/index.html'
    form_class = PromptForm
    success_url = reverse_lazy('home')  # asegúrate que redirige a la raíz

    def form_valid(self, form):
        UserPrompt.objects.create(user=self.request.user, prompt=form.cleaned_data['prompt'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_prompts'] = UserPrompt.objects.filter(user=self.request.user)
        return context


def home(request):
    return render(request, 'main_pages/index.html')
