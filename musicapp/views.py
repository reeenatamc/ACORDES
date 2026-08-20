from celery.result import AsyncResult
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView

from musicapp.forms import PromptForm
from musicapp.models import UserPrompt
from musicapp.tasks import generate_song


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Esto inicia sesión al usuario después de registrarse
            return redirect("home")  # Redirige al usuario a la página principal o donde desees
    else:
        form = UserCreationForm()

    return render(request, "auth/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")  # Redirige al home o donde quieras
    else:
        form = AuthenticationForm()

    return render(request, "auth/login.html", {"form": form})


# Clase que maneja el formulario de entrada y la creación de canciones generadas a partir de un prompt
class PromptFormView(FormView):
    template_name = "main_pages/index.html"  # Plantilla para renderizar la página
    form_class = PromptForm  # Formulario asociado a la vista
    success_url = reverse_lazy("home")  # Redirige al home después de una acción exitosa

    def form_valid(self, form):
        """Queue the generation and return straight away.

        Generation loads several hundred megabytes of models and takes minutes.
        Doing it here would hold an HTTP worker hostage for the whole time, so
        the request only records the prompt and hands the work to Celery.
        """
        if not self.request.user.is_authenticated:
            return redirect("login")

        prompt_text = form.cleaned_data["prompt"]
        user_prompt = UserPrompt.objects.create(user=self.request.user, prompt=prompt_text)

        task = generate_song.delay(user_prompt.id)
        self.request.session["last_generation_task"] = task.id

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Añade datos adicionales al contexto de la página, como los prompts anteriores del usuario.
        """
        context = super().get_context_data(**kwargs)
        context["user_prompts"] = UserPrompt.objects.filter(user=self.request.user)
        return context


def home(request):

    return render(request, "main_pages/index.html")


def generation_status(request, task_id):
    """Report the state of a queued generation so the page can poll it."""
    result = AsyncResult(task_id)
    payload = {"state": result.state}

    if result.successful():
        payload["result"] = result.result
    elif result.failed():
        payload["error"] = "generation failed"
    elif result.state == "PROGRESS":
        payload["step"] = (result.info or {}).get("step")

    return JsonResponse(payload)
